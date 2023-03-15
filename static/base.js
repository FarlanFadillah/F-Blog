window.onload = function() {
    document.body.style.opacity = 1; /* Tampilkan semua konten saat halaman selesai dimuat */
};


const myInput = document.getElementById("search_key");
const myLink = document.getElementById("search_pointer");
const myForm = document.getElementById("search-form");
const myHome = document.getElementById("home_link");

myLink.addEventListener("click", function() {
  const textValue = myInput.value;

  if (textValue.length > 0){
    myLink.href += textValue ;
  }else{
    myLink.href = myHome;
  }
  
  
});


myForm.addEventListener("submit", function(event) {
    event.preventDefault(); // menghentikan aksi bawaan dari form submit
    myLink.click(); // mengklik elemen a secara otomatis
});


function previewImage(event) {
  var reader = new FileReader(); // membuat objek FileReader
  reader.onload = function() {
    var preview = document.getElementById('image-preview');
    preview.src = reader.result; // mengganti gambar dengan gambar yang diunggah
  }
  reader.readAsDataURL(event.target.files[0]); // membaca file gambar yang diunggah
}
