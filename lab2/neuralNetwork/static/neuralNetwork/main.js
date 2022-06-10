$(document).ready(
  $('#submit-all').click(function(e){
    e.preventDefault();
    var my_data = $('#myAwesomeDropzone')[0].dropzone.files[0];
    //my_data.append("file", my_image)
    var formData= new FormData();
    formData.append('file', my_data);
    var form = $('#myAwesomeDropzone')[0];
    $.ajax({
      type:"POST",
      url: "analysis/",
      processData: false,
      data: formData,
      contentType: false,
      success: function(data) {
                $("#result").text(data["result"]);
      }
    });
  })
);
Dropzone.options.myAwesomeDropzone = {
  thumbnailWidth:"1000",
  thumbnailHeight:"1000",
  maxFiles: 1,
  autoProcessQueue: false,
  accept: function(file, done) {
    console.log("uploaded");
    done();
  },
  init: function() {
      var submitButton = document.querySelector("#submit-all")
      myAwesomeDropzone = this; // closure
      myAwesomeDropzone.on("addedfile", function(file) {
        file.previewElement.addEventListener("click", function() {
        myAwesomeDropzone.hiddenFileInput.click();
        $("#result").text("");
            });
        }),
     this.on("maxfilesexceeded", function(file) {
        this.removeAllFiles();
        this.addFile(file);
     });
  }
}

