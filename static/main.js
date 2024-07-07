/*=============== SHOW MENU ===============*/
const showMenu = (toggleId, navId) =>{
    const toggle = document.getElementById(toggleId),
          nav = document.getElementById(navId)
 
    toggle.addEventListener('click', () =>{
        // Add show-menu class to nav menu
        nav.classList.toggle('show-menu')
 
        // Add show-icon to show and hide the menu icon
        toggle.classList.toggle('show-icon')
    })
 }
 
 showMenu('nav-toggle','nav-menu')

//  function navigateToNewPage() {
//     // window.location.href = 'new_camera'; // Replace 'new-camera.html' with the path to your HTML file
//     window.location.href = "{% url 'videos:new-camera' %}";


// }
//live cam online
function youtubevalidation(url) {
    let embedUrl = url;

    if (url.includes('youtube.com/watch?v=')) {
        const videoId = url.split('v=')[1].split('&')[0];
        embedUrl = `https://www.youtube.com/embed/${videoId}`;
    } else if (url.includes('youtu.be/')) {
        const videoId = url.split('youtu.be/')[1];
        embedUrl = `https://www.youtube.com/embed/${videoId}`;
    }

    if (embedUrl) {
        const iframeContainer = document.getElementById('iframeContainer');
        iframeContainer.innerHTML = `
        <iframe src="${embedUrl}" allowfullscreen></iframe>
        <div class="countarea">
      <div class="count"></div>
      <button>count</button>
   </div>`;
    } else {
        alert('Please enter a valid URL.');
    }
}

// Function to handle adding video by URL
function addVideo() {
    const url = document.getElementById('url').value;

    // Check if the URL is part of the dataarray
    let isSpecialUrl = false;
    for (let i = 0; i < dataarray.length; i++) {
        if (dataarray[i][0].link === url) {
            populateSelector(i);
            isSpecialUrl = true;
            break;
        }
    }

    if (!isSpecialUrl) {
        youtubevalidation(url);
    }
}

// Populate selector with camera options
function populateSelector(index) {
    const selector = document.getElementById('camselector');
    selector.innerHTML = ''; // Clear existing options

    dataarray[index].forEach((cam, idx) => {
        const option = document.createElement('option');
        option.value = cam.link;
        option.textContent = cam.name;
        selector.appendChild(option);
    });

    // Add event listener for selector
    selector.addEventListener('change', function() {
        const selectedUrl = this.value;
        youtubevalidation(selectedUrl);
    });

    // Automatically display the first camera
    if (selector.options.length > 0) {
        selector.selectedIndex = 0;
        const event = new Event('change');
        selector.dispatchEvent(event);
    }
}

// Function to add HTML code directly
function addVideoByHtml() {
    const htmlCode = document.getElementById('HtmlCode').value;
    const iframeContainer = document.getElementById('iframeContainer');
    iframeContainer.innerHTML = htmlCode;
}

// Event listeners for buttons
document.getElementById('addVideoButton').addEventListener('click', addVideo);
document.getElementById('addHtmlButton').addEventListener('click', addVideoByHtml);

// Sample data
let op1 = {
    name: 'cam1',
    link: 'https://www.youtube.com/watch?v=vgFF35b567w'
}
let op2 = {
    name: 'cam2',
    link: 'https://youtu.be/ezLz5P1mqlY?si=gPCcy9FgGhOULs5y'
}
let op3 = {
    name: 'cam3',
    link: 'https://youtu.be/BO7mALtbs_k?si=UxG1P6ul88liVP-F'
}
let op4 = {
    name: 'cam4',
    link: 'https://youtu.be/8d633Z-Ez-0?si=Yin5miTxnFBueVh8'
}

const dataarray = [
    [op1, op2, op3, op4],
    [op4, op3, op2, op1]
];

