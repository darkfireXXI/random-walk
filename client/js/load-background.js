document.addEventListener("DOMContentLoaded", function()
    {
        const imgsFolder = 'imgs/backgrounds/';
        const images = ['apocalypse-explorer.jpg', 'aurora.jpg', 'color-panels.jpg', 'color-splash.jpg', 'space-explorer.jpg', 'tile-tunnel.jpg'];
        const randomImage = images[Math.floor(Math.random() * images.length)];
        document.body.style.backgroundImage = `url('${imgsFolder}${randomImage}')`;
    }
);


// document.addEventListener('DOMContentLoaded', function() {
//     // Simulated fetch of categories (replace with your actual API call)
//     fetchCategories()
//         .then(categories => {
//             displayCategories(categories);
//         })
//         .catch(error => {
//             console.error('Error fetching categories:', error);
//         });
// });

// // Function to fetch categories (replace with your actual fetch logic)
// function fetchCategories() {
//     // Simulated categories data
//     return new Promise((resolve, reject) => {
//         // Replace this with your actual fetch logic (API call)
//         setTimeout(() => {
//             const categories = ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'thing 5', 'Category 1', 'Category 2', 'Category 3', 'Category 4', 'thing 5', 'Category 1', 'Category 2', 'Category 3', 'Category 4', 'thing 5', 'Category 1', 'Category 2', 'Category 3', 'Category 4', 'thing 5', 'Category 1', 'Category 2', 'Category 3', 'Category 4', 'thing 5', 'Category 1', 'Category 2', 'Category 3', 'Category 4', 'thing 5'];
//             resolve(categories);
//         }, 1000); // Simulating delay
//     });
// }

// // Function to display categories in boxes
// function displayCategories(categories) {
//     const container = document.getElementById('categories-container');

//     categories.forEach(category => {
//         const categoryElement = document.createElement('div');
//         categoryElement.classList.add('category');
//         categoryElement.textContent = category;

//         // Add click event listener to each category box
//         categoryElement.addEventListener('click', function() {
//             // Handle click event (e.g., navigate to category page)
//             console.log('Clicked on category:', category);
//             // Example: window.location.href = '/category/' + encodeURIComponent(category);
//         });

//         container.appendChild(categoryElement);
//     });
// }
