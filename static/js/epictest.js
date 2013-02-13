function saveToServer(url, content, callback){
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open('POST', url, true);
  xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  xmlhttp.send("data="+content['data'])
};

function saveTest(){
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST", "/ajax?t='test'", true);
  xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  xmlhttp.send("hello=right");
};


var opts = {
  container: 'epiceditor',
  basePath: 'static/epiceditor',
  clientSideStorage: true,
  localStorageName: 'epiceditor',
  useNativeFullsreen: true,
  parser: marked,
  file: {
    name: 'epiceditor',
    defaultContent: '',
    autoSave: 100
  },
  theme: {
    base:'/themes/base/epiceditor.css',
    preview:'/themes/preview/preview-dark.css',
    editor:'/themes/editor/epic-dark.css'
  },
  focusOnLoad: false,
  shortcut: {
    modifier: 18,
    fullscreen: 70,
    preview: 80
  }
}

var editor = new EpicEditor(opts);

function loadEditor(){
  editor.load(function(){
    console.log("Editor loaded successfully.");
  });
};

function unloadEditor(){
  editor.unload(function(){
    console.log("Editor unloaded successsfully.");
  });
};

function openFile(){
  editor.open('some file'); // Opens a file when the user clicks this button
  console.log('Now open a file');
};

function exportFile(){
  var theContent = editor.exportFile("epiceditor","application/json");
  saveToServer('/ajax?t=save', {data:theContent}, function () {
    console.log('Data was saved to the database.');
  });
};

function sendContent(){

}
