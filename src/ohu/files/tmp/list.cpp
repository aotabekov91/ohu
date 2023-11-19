public void show_file(String Path)
{
        //initialization of fileSystem Model and Dir path 
       QFileSystemModel std = new QFileSystemModel();
       	QDir dir = new QDir(path);
 
        // to arrange the items 
        ui.listView.setUniformItemSizes(true);
 
        // join the model to the listView
         ui.listView.setModel(std);
       	ui.listView.setRootPath(std.index(dir.path()));
 
}

also

https://stackoverflow.com/questions/7016877/qt-browsing-filesystem-with-qlistview-and-qfilesystemmodel-how-to-higlight-fir
