import hou, os, datetime, pathlib, re, subprocess
import pymongo
from hutil.Qt import QtCore, QtUiTools, QtWidgets, QtGui


class OP_Browser:
    def __init__(self):
        ui_file_path = "R:/apexTools/op_houdini_browser.ui"
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile(ui_file_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        self.opBrowser = loader.load(ui_file)
            
        # Environment Variables
        db_connection = os.getenv("OPENPYPE_MONGO")
        db_name = os.getenv("AVALON_DB")
        av_project = os.getenv("AVALON_PROJECT")
        av_task = os.getenv("AVALON_TASK")
        
        global client, db
        client = pymongo.MongoClient(db_connection)
        db = client.get_database(db_name)
            
        # Get local user
        self.user = self.getUser(client)
        
        # Populate Projects from the current database
        self.project_list = self.projects(db, av_project)
        
        # Check if the current project is a Library
        self.libraryProject(None, db)
        self.opBrowser.projects_combo.currentIndexChanged.connect(lambda index, db=db: self.libraryProject(index, db))
        
        # Populate Project Code from the current project -- Change the project code whene Project is changed
        self.projectCode(None, db)
        self.opBrowser.projects_combo.currentIndexChanged.connect(lambda index, db=db: self.projectCode(index, db))
        
        # Populate Sequence list from the current project -- Change the Sequence list when the Project is changed
        self.default_sequence(None, db)
        self.opBrowser.projects_combo.currentIndexChanged.connect(lambda index, db=db: self.sequences(index, db))
        
        # Populate Shot list from the current project -- Change Shot list when the Sequence is changed
        self.default_shot(None,db)
        self.opBrowser.sequence_combo.currentIndexChanged.connect(lambda index, db=db: self.shots(index, db))

        # Populate Family list from current project -- Change the Family list when the Shot is changed
        self.families(None, db)
        self.opBrowser.shot_combo.currentIndexChanged.connect(lambda index, db=db: self.families(index, db))

        # Populate the table based on the subsets from the current family
        self.browser(None, db)
        self.opBrowser.family_combo.currentIndexChanged.connect(lambda index, db=db: self.browser(index, db))
        
        #name,version,representation = None        
        self.opBrowser.load_button.clicked.connect(self.loadAsset)
        
        # Get attributes from the project drop down boxes
        self.comboAttributes()
        
        # Store the selected versions that were imported to the scene
        self.selected_versions = {}
        
        # Check if there are updates to the assets based on the versions imported
        self.checkForUpdate()
        self.opBrowser.family_combo.currentIndexChanged.connect(self.checkForUpdate)
        
        self.reviewButtonDisplay()
        self.opBrowser.family_combo.currentIndexChanged.connect(self.reviewButtonDisplay)
        
        self.opBrowser.review_button.clicked.connect(self.reviewAsset)
        
        self.loadToCameraButtonDisplay()
        self.opBrowser.family_combo.currentIndexChanged.connect(self.loadToCameraButtonDisplay)
        
        self.opBrowser.load_to_cam_button.clicked.connect(self.loadToCamera)
        
        self.populateInventory()
        self.opBrowser.delete_assets_button.clicked.connect(self.deleteAssets)
        
        self.opBrowser.check_updates_button.clicked.connect(self.checkForInventoryUpdates)
        # FUTURE -- Populate loaded assets table 
    
    def reviewButtonDisplay(self):
        family = self.opBrowser.family_combo.currentText()

        if family == "review" or family == "render" or family == "plate":
            self.opBrowser.review_button.resize(74,25)
        else:
            self.opBrowser.review_button.resize(0,0)
    
            
    def loadToCameraButtonDisplay(self):
        family = self.opBrowser.family_combo.currentText()
        
        if family == "plate":
            self.opBrowser.load_to_cam_button.resize(120,25)
        else:
            self.opBrowser.load_to_cam_button.resize(0,0)
            
            
    def getUser(self, client):
        db_op = client.get_database("openpype")
        settings_collection = db_op.get_collection("settings")
        local_doc = settings_collection.find_one({"type": "local_settings"})["data"]["general"]
        local_user = local_doc.get("username")
        self.opBrowser.db_user_label.setText(local_user)

        return local_user
        

    def projects(self, db, av_project):
        # Populate the Project List
        projects = db.list_collection_names()
        self.opBrowser.projects_combo.addItems(projects)
        
        # Set the default project to current
        index = projects.index(av_project)
        self.opBrowser.projects_combo.setCurrentIndex(index)
  
        
    def libraryProject(self, index, db):
        # Check if project is a library
        current_project = self.comboAttributes()[0]
        project_doc = db.get_collection(current_project).find_one({"type": "project"})["data"]
        project_library = project_doc.get("library_project")
        
        if project_library == True:
            width, height = 32, 25
            self.opBrowser.library_label.setMinimumSize(width, height)
            self.opBrowser.library_label.setMaximumSize(width, height)
            
        if project_library == False:
            width, height = 0,0
            self.opBrowser.library_label.setMaximumSize(width, height)
            self.opBrowser.library_label.setMinimumSize(width, height)
        
        
    def projectCode(self, index, db):
        # Get current project
        current_project = self.comboAttributes()[0]
        
        project_collection = db.get_collection(current_project)
        project_doc = project_collection.find_one({"type": "project"})["data"]
        
        # Store the project code as a global variable and apply it
        global project_code
        project_code = project_doc.get("code")
        self.opBrowser.db_job_code_label.setText(project_code)
        

    def default_sequence(self, index, db):
        # Get _id of the project document
        current_project = self.comboAttributes()[0]
        project_collection = db.get_collection(current_project)
        project_doc = project_collection.find_one({"type": "project"})
        project_id = project_doc.get("_id")
        
        # Get parent id of all assets in the collection
        sequences = project_collection.find({"parent": project_id, "data.parents":{"$size":0}})
        
        # Get names of sequences and store them in a list
        names = []
        for seq in sequences:
            names.append(seq["name"])
        
        # Clear the list of sequences and add the found documents to the sequnces list
        self.opBrowser.sequence_combo.clear()
        self.opBrowser.sequence_combo.addItems(names)

        # Set the default sequence to current
        seq_name = os.getenv("AVALON_ASSET").split("_")[0]
        index = names.index(seq_name)
        self.opBrowser.sequence_combo.setCurrentIndex(index)
        
        return
        
        
    def sequences(self, index, db):
        # Get _id of the project document
        current_project = self.comboAttributes()[0]
        project_collection = db.get_collection(current_project)
        project_doc = project_collection.find_one({"type": "project"})
        project_id = project_doc.get("_id")
        
        # Get parent id of all assets in the collection
        sequences = project_collection.find({"parent": project_id, "data.parents":{"$size":0}})
        names = []
        for seq in sequences:
            names.append(seq["name"])
        
        # Clear the list of sequences and add the found documents to the sequnces list
        self.opBrowser.sequence_combo.clear()
        self.opBrowser.sequence_combo.addItems(names)
        
        return
        
    
    def default_shot(self, index, db):
        # Get the current project
        current_project = self.comboAttributes()[0]
        current_sequence = self.comboAttributes()[1]
        project_collection = db.get_collection(current_project)
        
        # Get all of the shots under the current sequence and sort them
        shots = project_collection.find({"data.parents": current_sequence, "type": "asset"})
        shot_names = []
        for shot in shots:
            shot_names.append(shot["name"])
        shot_names.sort()
        
        # Clear and populate the shot combo box with list of shots
        self.opBrowser.shot_combo.clear()
        self.opBrowser.shot_combo.addItems(shot_names)
        
        # Set the shot_combo box to the currently opened shot
        current_shot = os.getenv("AVALON_ASSET")
        index = shot_names.index(current_shot)
        self.opBrowser.shot_combo.setCurrentIndex(index)
        
        return
        

    def shots(self, index, db):
        # Get the current sequence
        current_project = self.comboAttributes()[0]
        current_sequence = self.comboAttributes()[1]
        project_collection = db.get_collection(current_project)
        
        # Get all shots related to the current sequence and store them in a sorted list
        shots = project_collection.find({"data.parents": current_sequence, "type": "asset"})
        shot_names = []
        for shot in shots:
            shot_names.append(shot["name"])
        shot_names.sort()
        
        # Clear the list of shots and add the found documents to the shots list
        self.opBrowser.shot_combo.clear()
        self.opBrowser.shot_combo.addItems(shot_names)
        
        return


    def families(self, index, db):
        # Get _id of the shot document
        current_project = self.comboAttributes()[0]
        project_collection = db.get_collection(current_project)
        
        current_shot = self.comboAttributes()[2]
        shot_doc = project_collection.find_one({"name": current_shot})
        shot_id = shot_doc["_id"]
        
        # Get parent id of all assets in the collection similar to the parents object id
        shot_families = project_collection.find({"parent": shot_id, "type": "subset"})
        
        # Initialize the families attribute into a list and store all families to it
        families = []
        for family in shot_families:
            families.append(family["data"]["family"])
        families.sort()
        
        # Clear the list of sequences and add the found documents to the Family list
        self.opBrowser.family_combo.clear()
        self.opBrowser.family_combo.addItems(set(families))
        
        # If there are no published assets, this gets printed in the combo box instead
        if families == []:
            self.opBrowser.family_combo.addItems(["No Families"])
        

    def browser(self, index, db):
        # Get _id of shot document
        current_project = self.comboAttributes()[0]
        project_collection = db.get_collection(current_project)
        
        # Get the shot ids
        current_shot = self.comboAttributes()[2]
        shot_doc = project_collection.find_one({"name": current_shot})
        shot_id = shot_doc.get("_id")
              
        current_family = self.opBrowser.family_combo.currentText()
        
        # Get all subsets derived from the family
        shot_subsets = list(project_collection.find({"parent": shot_id, "type": "subset", "data.family": current_family}))
        
        # Get amount of subsets to be used as rows
        subset_index = len(shot_subsets)
        self.opBrowser.browser_table.setRowCount(subset_index)
        
        paths = []
        
        # Set the row count to iterate over
        row = 0
        for subset in shot_subsets:
            
            # Resize the first cell in the row to be small (It's going to be used as a color cell)
            self.opBrowser.browser_table.resizeColumnToContents(0)
            
            
            # NAMES ---------------
            subset_name = [subset["name"]]
            
            for string in subset_name:
                name = string.replace(current_family, "")
            
            name_item = QtWidgets.QTableWidgetItem(name)
            self.opBrowser.browser_table.setItem(row, 1, name_item)
            # ---------------------
            
            
            # VERSIONS ------------
            # Get _ids of all subsets under the current family
            subset_ids = [subset["_id"]]
            
            # Create Combo box for the versions to reside 
            self.version_combo = QtWidgets.QComboBox()
            
            # Find all of the documents associated with the current subset
            version_docs = project_collection.find({"type": "version", "parent": {"$in": subset_ids}})
            versions = []

            # Add versions to the combo box
            for version in version_docs:
                versions.append(str(version["name"]))
            self.version_combo.addItems(versions)
            
            max_version = max(versions)
            version_index = versions.index(max_version)
            self.version_combo.setCurrentIndex(version_index)
            
            # Add versions combo box to the table cell associated with versions
            version_item = QtWidgets.QTableWidgetItem()
            self.opBrowser.browser_table.setItem(row, 2, version_item)
            self.opBrowser.browser_table.setCellWidget(row, 2, self.version_combo)
            # ---------------------
            
            
            # REPRESENTATIONS -----
            version_docs = project_collection.find({"type": "version"})
            
            # Create combo box for the representations to reside
            self.rep_combo = QtWidgets.QComboBox()
            
            # Find all of the documents associated with the current subset
            rep_docs = project_collection.find({"type": "representation", "parent": version["_id"]})
            
            # Get the name of the representation and add it to the combo box
            for rep in rep_docs:
                representations = [str(rep["context"]["ext"])]
                self.rep_combo.addItems(representations)
            
            # Place the representation combo box into the appropriate cell
            rep_item = QtWidgets.QTableWidgetItem()
            self.opBrowser.browser_table.setItem(row, 3, rep_item)
            self.opBrowser.browser_table.setCellWidget(row, 3, self.rep_combo)
            # ---------------------
            
            
            # Frames --------------
            subset_ids = [subset["_id"]]
            version_docs = project_collection.find({"type": "version", "parent": {"$in": subset_ids}})
            
            for f in version_docs:
                start_frame = str(int(float(f["data"]["frameStart"])))
                end_frame = str(int(float(f["data"]["frameEnd"])))
            
            frames = start_frame + ' - ' + end_frame
            frames_item = QtWidgets.QTableWidgetItem(frames)
            self.opBrowser.browser_table.setItem(row, 4, frames_item)
            # ---------------------
            
            
            # PUBLISHED BY --------
            version_docs = project_collection.find({"type": "version"})
            version_ids = []
            for version in version_docs:
                version_ids.append(version["_id"])
            
            # Create the list to populate later
            publish_items = []
            
            # Get the representation documents that have the same parent id as version documents
            for version_id in version_ids:
                pub_docs = project_collection.find({"type": "representation", "parent": version_id})
            
            # Initialize the pb list for each version
            pb = []  
            
            # Get the context and user user data, and append to the pb list
            for pub in pub_docs:
                context = pub.get("context", {})
                user = context.get("user", "")
                pb.append(user)

            publish_item = QtWidgets.QTableWidgetItem(', '.join(pb))
            publish_items.append(publish_item)

            for i, publish_item in enumerate(publish_items):
                self.opBrowser.browser_table.setItem(row + i, 6, publish_item) 
            # ---------------------

            
            # PATH & TIME ---------
            b_root = os.getenv("OPENPYPE_PROJECT_ROOT_WORK")
            b_proj, b_sequence, b_shot, b_family = self.comboAttributes()
            b_name = self.opBrowser.browser_table.item(row, 1).text()
            b_version = self.opBrowser.browser_table.cellWidget(row, 2).currentText()
            b_subset = b_family + b_name
            
            # Construct the folder path
            path = f"{b_root}{b_proj}/{b_sequence}/{b_shot}/publish/{b_family}/{b_subset}/v{b_version:0>3}/"
            
            b_path = "Path: " + path
            path_item = QtWidgets.QTableWidgetItem(b_path)
            self.opBrowser.browser_table.setItem(row, 7, path_item)
            
            files = os.walk(path)
            
            path_time = pathlib.Path(path)
            m_time = path_time.stat().st_mtime
            time = datetime.datetime.fromtimestamp(m_time)
            string_time = time.strftime("%B %d, %Y - %H:%M MST")
            
            time_item = QtWidgets.QTableWidgetItem(string_time)
            self.opBrowser.browser_table.setItem(row, 5, time_item)
            # ---------------------
            
            row += 1

    def getSelectedRows(self):
        selected_rows = []
        selected_items = None
        if self.opBrowser.browser_table.selectionModel().hasSelection():
            selected_items = self.opBrowser.browser_table.selectedItems()
        
        if self.opBrowser.inventory_table.selectionModel().hasSelection():
            selected_items = self.opBrowser.inventory_table.selectedItems()
        
        for item in selected_items:
            row = item.row()
            if row not in selected_rows:
                selected_rows.append(row)
                set(selected_rows)    
        
        return selected_rows
    
    def getAssetPaths(self):
        
        selected_rows = self.getSelectedRows()

        folder_path = []
        init_path = []
        ext = []
        p_shot = []
        p_family = []
        p_subset = []
        p_version = []
        p_name = []
        
        for row in selected_rows:
            if row >= 0:
                root = os.getenv("OPENPYPE_PROJECT_ROOT_WORK")
                proj, sequence, shot, family = self.comboAttributes()
                name, version, representation, published_by, frames = self.rowAttributes(row)
                start_frame = int(float(frames[0]))
                end_frame = int(float(frames[1]))
                frame_count = end_frame - start_frame
                subset = family+name
                res_height = self.cameraResolution()[0]
                res_width = self.cameraResolution()[1]
                
                folder_path.append(f"{root}{proj}/{sequence}/{shot}/publish/{family}/{subset}/v{version:0>3}/")
                init_path.append(f"{root}{proj}/{sequence}/{shot}/publish/{family}/{subset}/v{version:0>3}/{project_code}_{shot}_{subset}_v{version:0>3}")
                
                ext.append(representation)
                p_shot.append(shot)
                p_family.append(family) 
                p_subset.append(subset)
                p_version.append(version)
                p_name.append(name)

                
        return init_path, folder_path, ext, p_shot, p_subset, p_family, p_version
 
        
    def loadAsset(self):

        init_path, folder_path, representation, shot, subset, family, version = self.getAssetPaths()
        proj = self.comboAttributes()[0]
        seq = self.comboAttributes()[1]
        
        obj = hou.node('/obj')
        img = hou.node('/img')
        container = hou.node('/obj/ASSETS')
        img_container = hou.node('/img/COMP')
        op_node = None

        path_count = len(init_path)
        
        for p in range(path_count):
            if container == None:
                op_container = obj.createNode('subnet', node_name="ASSETS").setUserData("nodeshape", "ayon")
                container = hou.node(op_container)

            container_name = f"{shot[p]}_{subset[p]}_v{version[p]:0>3}_CON"
            container_path = f"/obj/ASSETS/{container_name}"
            img_container_path = f"/img/{shot[p]}_COMP"
            asset_name = f"{shot[p]}_{subset[p]}_v{version[p]:0>3}"
            node_check = hou.node(f"/obj/ASSETS/{container_name}/{asset_name}")
            
            file_count = self.countFiles(folder_path[p], representation[p])
            
            if representation[p] == "bgeo.sc":
                if file_count > 1:
                    bgeo_path = init_path[p] + ".$F4." + representation[p]
                else: 
                    bgeo_path = init_path[p] + "." + representation[p]
                    
                if node_check == None:
                    geo = container.createNode('geo', node_name = container_name)

                    ptg = geo.parmTemplateGroup()
                    op_folder = self.parmTemplates(proj, seq, shot[p], family[p], subset[p], version[p], representation[p])                    
                    ptg.append(op_folder)
                    geo.setParmTemplateGroup(ptg)
                    
                    file = geo.createNode('file', node_name = asset_name)
                    file.setParms({"file": bgeo_path})
                    
                    op_node = container_path
                    
                    self.addToInventory(proj, subset[p], version[p], family[p], representation[p], op_node)
                else:
                    print("Asset is already imported")
        
            if representation[p] == "abc" and family[p] != "camera":
                abc_path = init_path[p] + '.' + representation[p]
            
                if node_check is None:
                    geo = container.createNode('geo', node_name = container_name)
                    
                    ptg = geo.parmTemplateGroup()
                    op_folder = self.parmTemplates(proj, seq, shot[p], family[p], subset[p], version[p], representation[p]) 
                    ptg.append(op_folder)
                    geo.setParmTemplateGroup(ptg)
                    
                    abc = geo.createNode('alembic', node_name = asset_name)
                    abc.setParms({"fileName": abc_path})
                    
                    op_node = container_path

                    self.addToInventory(proj, subset[p], version[p], family[p], representation[p], op_node)
                else:
                    print("Asset is already imported")
                    
            if representation[p] == "abc" and family[p] == "camera":
                abc_path = init_path[p] + '.' + representation[p]
                cam_check = hou.node(f"/obj/{asset_name}")
                
                res_width = self.cameraResolution()[1]
                res_height = self.cameraResolution()[0]
                
                if cam_check is None:
                    abc = obj.createNode('alembicarchive', node_name = asset_name)
                    
                    ptg = abc.parmTemplateGroup()
                    op_folder = self.parmTemplates(proj, seq, shot[p], family[p], subset[p], version[p], representation[p]) 
                    ptg.append(op_folder)
                    abc.setParmTemplateGroup(ptg)
                    
                    abc.setParms({"fileName": abc_path})
                    abc.parm('/obj/' + str(abc) + '/buildHierarchy').pressButton()
                    
                    cam_path = f"{obj}/{asset_name}/{shot[p]}_{subset[p]}_01__{subset[p]}/{shot[p]}_{subset[p]}_01__{subset[p]}Shape"
                    cam = hou.node(cam_path)
                    cam.setParms({"resx": res_width, "resy": res_height})
                    
                    op_node = container_path
                    
                    self.addToInventory(proj, subset[p], version[p], family[p], representation[p], op_node)
                else:
                    print("Camera is already imported")
                    
            if representation[p] == "vdb":
                vdb_path = init_path[p] + '.$F4.' + representation[p]
                
                if node_check == None:
                    geo = obj.createNode('geo', node_name = container_name)
                    
                    ptg = geo.parmTemplateGroup()
                    op_folder = self.parmTemplates(proj, seq, shot[p], family[p], subset[p], version[p], representation[p]) 
                    ptg.append(op_folder)
                    geo.setParmTemplateGroup(ptg)
                    
                    vdb = geo.createNode('file', node_name = asset_name)
                    vdb.parm({"file": vdb_path})
                    
                    op_node = hou.node(geo)
                    
                    self.addToInventory(proj, subset[p], version[p], family[p], representation[p], op_node)
                    
            if representation[p] == "exr" or representation[p] == 'jpg' or representation[p] == 'png':
                file_count = self.countFiles(folder_path[p], representation[p])
                if file_count > 1:
                    img_path = init_path[p] + '.$F4.' + representation[p]
                else:
                    img_path = init_path[p] + '.' + representation[p]

                cop_check = hou.node(f"/img/{shot[p]}_COMP/{asset_name}")
                
                if img_container == None:
                    op_cop_container = img.createNode('img', node_name = f'{shot[p]}_COMP')
                    container = hou.node(str(op_cop_container))
                    
                if cop_check == None:
                    img = op_cop_container.createNode('file', node_name = asset_name)
                    img.setParms({"filename1": img_path})
                    
                    ptg = img.parmTemplateGroup()
                    op_folder = self.parmTemplates(proj, seq, shot[p], family[p], subset[p], version[p], representation[p]) 
                    ptg.append(op_folder)
                    img.setParmTemplateGroup(ptg)
                    
                    op_node = img_container_path
                    
                    self.addToInventory(proj, subset[p], version[p], family[p], representation[p], op_node)
                else:
                    print("Image Sequence is already imported")
            
            self.changeStatus()
            self.checkForUpdate()
            
            
    def addToInventory(self, proj, subset, version, family, representation, op_node):
        self.opBrowser.inventory_table.resizeColumnToContents(0)
        
        row_count = self.opBrowser.inventory_table.rowCount()
        if row_count == 0:
            row = 0
        if row_count > 0:
            row = row_count

        self.opBrowser.inventory_table.insertRow(row)
        
        # STATUS ----------------
        status_widget = QtWidgets.QWidget()
        status_widget.setStyleSheet("background-color: rgb(60, 233, 186);")
        self.opBrowser.inventory_table.setCellWidget(row, 0, status_widget)
        # -----------------------
        
        # PROJECT ---------------
        project_item = QtWidgets.QTableWidgetItem(proj)
        self.opBrowser.inventory_table.setItem(row, 1, project_item)
        self.opBrowser.inventory_table.resizeColumnToContents(1)
        # -----------------------
        
        # NAME ------------------
        subset_item = QtWidgets.QTableWidgetItem(subset)
        self.opBrowser.inventory_table.setItem(row, 2, subset_item)
        self.opBrowser.inventory_table.resizeColumnToContents(2)
        # -----------------------
        
        # VERSION ---------------
        version_item = QtWidgets.QTableWidgetItem(f"v{version:0>3}")
        self.opBrowser.inventory_table.setItem(row, 3, version_item)
        self.opBrowser.inventory_table.resizeColumnToContents(3)
        # -----------------------
        
        # FAMILY ----------------
        family_item = QtWidgets.QTableWidgetItem(family)
        self.opBrowser.inventory_table.setItem(row, 4, family_item)
        self.opBrowser.inventory_table.resizeColumnToContents(4)
        # -----------------------
        
        # REPRESENTATION --------
        rep_item = QtWidgets.QTableWidgetItem(representation)
        self.opBrowser.inventory_table.setItem(row, 5, rep_item)
        self.opBrowser.inventory_table.resizeColumnToContents(5)
        # -----------------------
        
        # NODE PATH -------------
        node_item = QtWidgets.QTableWidgetItem(op_node)
        self.opBrowser.inventory_table.setItem(row, 6, node_item)
        self.opBrowser.inventory_table.resizeColumnToContents(6)
        # -----------------------
    
        
    def populateInventory(self):
        assets = hou.node('/obj/ASSETS')
        children = assets.children()
        
        
        if len(children) > 0:
            for c in children:
                proj = c.evalParm("proj")
                subset = c.evalParm("subset")
                version = c.evalParm("version")
                family = c.evalParm("family")
                representation = c.evalParm("representation")
                node = c.path()

                self.addToInventory(proj, subset, version, family, representation, node)
            
        
    def deleteAssets(self):
        selected_rows = self.getSelectedRows()
        
        for row in selected_rows:
            if row >= 0:
                node_path = self.opBrowser.inventory_table.item(row, 6).text()
                node = hou.node(node_path)
                hou.Node.destroy(node)
                
                self.opBrowser.inventory_table.removeRow(row)
                
        
    def reviewAsset(self):
        init_path = self.getAssetPaths()[0] 
        folder_path = self.getAssetPaths()[1]
        representation = self.getAssetPaths()[2]

        rv = 'C:/Program Files/Shotgun/RV-2021.0.1/bin/rv.exe'
        mplay = os.getenv('H') + '/bin/mplay.exe'
        
        path_count = len(init_path)
        
        for p in range(path_count):
            file_count = self.countFiles(folder_path[p], representation[p])
    
            if representation[p] == "mp4" or representation[p] == "mov":
                vid_path = init_path[p] + '_h264.' + representation[p]
    
                subprocess.Popen([rv, vid_path])
    
            if representation[p] == "exr" or representation[p] == "png" or representation[p] == "jpg":
                if file_count == 1:
                    img_path = init_path[p] + '.' + representation[p]
                    subprocess.Popen([rv, img_path])
                
                if file_count > 1:
                    img_seq_path = init_path[p] + '.%04d.' + representation[p]
                    subprocess.Popen([rv, img_seq_path])

    def parmTemplates(self, proj, seq, shot, family, subset, version, representation):
        
        op_folder = hou.FolderParmTemplate(name='op_data', label='OP Data', folder_type=hou.folderType.Tabs, is_hidden=False)
        op_folder.addParmTemplate(hou.StringParmTemplate('proj', 'Project', default_value=([proj]), num_components = 1, string_type=hou.stringParmType.Regular))
        op_folder.addParmTemplate(hou.StringParmTemplate('seq', 'Sequence', default_value=([seq]), num_components = 1, string_type = hou.stringParmType.Regular))
        op_folder.addParmTemplate(hou.StringParmTemplate('shot', 'shot', default_value=([shot]), num_components = 1, string_type = hou.stringParmType.Regular))
        op_folder.addParmTemplate(hou.StringParmTemplate('family', 'family', default_value=([family]), num_components = 1, string_type = hou.stringParmType.Regular))
        op_folder.addParmTemplate(hou.StringParmTemplate('subset', 'subset', default_value=([subset]), num_components = 1, string_type = hou.stringParmType.Regular))
        op_folder.addParmTemplate(hou.StringParmTemplate('version', 'Version', default_value=([version]), num_components = 1, string_type = hou.stringParmType.Regular))
        op_folder.addParmTemplate(hou.StringParmTemplate('representation', 'Representation', default_value=([representation]), num_components = 1, string_type = hou.stringParmType.Regular))
        
        return op_folder
        
    def loadToCamera(self):
        init_path = self.getAssetPaths()[0]
        representation = self.getAssetPaths()[2]
        
        bg_path = f"{init_path[0]}.$F4.{representation[0]}"
        cam = hou.selectedNodes()[0]

        if cam == None:
            print("No camera selected")
        else:
            cam.setParms({"vm_background": bg_path})
                
            
    def changeStatus(self):

        selected_rows = self.getSelectedRows()
        
        for row in selected_rows:
            status_widget = QtWidgets.QWidget()
            status_widget.setStyleSheet("background-color: rgb(60, 233, 186);")
            self.opBrowser.browser_table.setCellWidget(row, 0, status_widget)
            
        
    def checkForUpdate(self):
        for r in range(self.opBrowser.browser_table.rowCount()):
            row = r
            
            proj, sequence, shot, family = self.comboAttributes()
            name, version, representation, published_by, frames = self.rowAttributes(row)
            start_frame = int(float(frames[0]))
            end_frame = int(float(frames[1]))
            frame_count = end_frame - start_frame
            version_count = self.opBrowser.browser_table.cellWidget(row, 2).count()
            version_list = []
            
            for v in range(version_count):
                version_list.append(v + 1)
            
            max_version = str(max(version_list))
            container_path = f"/obj/ASSETS/{shot}_{family+name}_v{version:0>3}_CON"
            container_check = hou.node(container_path)
            
            status_widget = QtWidgets.QWidget()
            
            if container_check is not None:
                if version < max_version:
                    status_widget.setStyleSheet("background-color: rgb(255,110,70);")
                    
                if version == max_version:
                    status_widget.setStyleSheet("background-color: rgb(60, 233, 186);")
            
            if container_check is None:
                    status_widget.setStyleSheet("")
                    
            self.opBrowser.browser_table.setCellWidget(row, 0, status_widget)

            
    def checkForInventoryUpdates(self):
        for r in range(self.opBrowser.inventory_table.rowCount()):
            row = r
            
            path = self.opBrowser.inventory_table.item(row, 6).text()
            check_path = hou.node(path)
            
            status_widget = QtWidgets.QWidget()

            if check_path == None:
                status_widget.setStyleSheet("background-color: rgb(200,50,50);")
                self.opBrowser.inventory_table.setCellWidget(row, 0, status_widget)

    def comboAttributes(self):
        
        proj = self.opBrowser.projects_combo.currentText()
        sequence = self.opBrowser.sequence_combo.currentText()
        shot = self.opBrowser.shot_combo.currentText()
        family = self.opBrowser.family_combo.currentText()

        return proj, sequence, shot, family


    def rowAttributes(self, row):

        name = self.opBrowser.browser_table.item(row, 1).text()
        version = self.opBrowser.browser_table.cellWidget(row, 2).currentText()
        representation = self.opBrowser.browser_table.cellWidget(row, 3).currentText()
        published_by = self.opBrowser.browser_table.item(row, 6).text()
        frames = self.opBrowser.browser_table.item(row, 4).text().split(" - ")

        return name, version, representation, published_by, frames


    def cameraResolution(self):
        
        proj = self.comboAttributes()[0]
        shot = self.comboAttributes()[2]

        proj_doc = db.get_collection(proj)
        shot_doc = proj_doc.find({"type": "asset", "name": shot})
        
        for sd in shot_doc:
            res_height = sd["data"]["resolutionHeight"]
            res_width = sd["data"]["resolutionWidth"]
        
        return res_height, res_width

        
    def countFiles(self, folder_path, representation):
        file_count = 0
        for fp in os.listdir(folder_path):
            if fp.endswith(representation):
                file_count += 1

        return file_count
            
        
def onCreateInterface():
    ui_created = None
    if not ui_created:
        window = OP_Browser()
        return window.opBrowser
    else:
        return None
