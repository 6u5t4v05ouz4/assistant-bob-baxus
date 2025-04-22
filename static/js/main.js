/**
 * Main JavaScript file for whisky recommendation app
 */

// Show loading spinner
function showLoader() {
    document.getElementById('loader').style.display = 'block';
    document.getElementById('content').style.display = 'none';
}

// Hide loading spinner
function hideLoader() {
    document.getElementById('loader').style.display = 'none';
    document.getElementById('content').style.display = 'block';
}

// Format currency
function formatCurrency(value) {
    if (!value) return 'N/A';
    return '$' + parseFloat(value).toFixed(2);
}

// Toggle recommendation cards between grid and list view
function toggleView(viewType) {
    const recCards = document.querySelectorAll('.recommendation-container');
    
    if (viewType === 'grid') {
        recCards.forEach(card => {
            card.classList.remove('col-12');
            card.classList.add('col-md-6', 'col-lg-4');
        });
        document.getElementById('gridBtn').classList.add('active');
        document.getElementById('listBtn').classList.remove('active');
    } else {
        recCards.forEach(card => {
            card.classList.remove('col-md-6', 'col-lg-4');
            card.classList.add('col-12');
        });
        document.getElementById('listBtn').classList.add('active');
        document.getElementById('gridBtn').classList.remove('active');
    }
}

// Initialize material icons
function initIcons() {
    const iconElements = document.querySelectorAll('.material-icons');
    iconElements.forEach(icon => {
        // This would be where we'd initialize any icon library if needed
        // Since we're using Bootstrap icons, they should work out of the box
    });
}

// Handle form submission with validation
function setupFormValidation() {
    const form = document.getElementById('usernameForm');
    if (form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                showLoader();
            }
            form.classList.add('was-validated');
        }, false);
    }
}

// Initialize tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Setup form validation
    setupFormValidation();
    
    // Initialize tooltips
    initTooltips();
    
    // Initialize icons if needed
    initIcons();
    
    // Hide loader on page load
    hideLoader();
    
    // Initialize charts if we're on the recommendations page
    const barStatsElement = document.getElementById('barStatsData');
    if (barStatsElement) {
        const barStats = JSON.parse(barStatsElement.textContent);
        if (barStats.spirit_types) {
            createSpiritChart(barStats.spirit_types);
        }
        if (barStats.brands_count) {
            createBrandChart(barStats.brands_count);
        }
        if (barStats.price_distribution) {
            createPriceChart(barStats.price_distribution);
        }
    }
    
    // Setup view toggle buttons
    const gridBtn = document.getElementById('gridBtn');
    const listBtn = document.getElementById('listBtn');
    
    if (gridBtn && listBtn) {
        gridBtn.addEventListener('click', function() {
            toggleView('grid');
        });
        
        listBtn.addEventListener('click', function() {
            toggleView('list');
        });
    }
});
