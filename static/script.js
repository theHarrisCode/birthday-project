$( ".bodyClass" ).on


// Get all date containers
const dateContainers = document.querySelectorAll('.day-container');

// Add click event listeners to each date container
dateContainers.forEach(container => {
    const dateTitle = container.querySelector('.date-title');
    const detailsContainer = container.querySelector('.body-container');

    // Add click event listener to the date title
    dateTitle.addEventListener('click', () => {
        // Toggle the visibility of the details container
        if (detailsContainer.style.display === 'none' || detailsContainer.style.display === '') {
            detailsContainer.style.display = 'flex';
        } else {
            detailsContainer.style.display = 'none';
        }
    });
});

