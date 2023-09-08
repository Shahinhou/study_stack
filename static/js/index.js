function defold(element){
    //var coll = document.getElementsByClassName("collapsible");
    console.log('clicked');
    console.log(element.nextElementSibling);

    var content = (element.nextElementSibling);

    element.classList.toggle("active");
    
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  }


