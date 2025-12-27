function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
    ev.target.classList.add('dragging');
}

// Add event listener to remove dragging class on dragend
document.addEventListener('dragend', function (ev) {
    if (ev.target.classList.contains('kanban-card')) {
        ev.target.classList.remove('dragging');
    }
});

function drop(ev, newStage) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    var element = document.getElementById(data);
    var requestId = data.replace('req-', '');

    // Highlight removal (if we add dragging over later)
    // ev.target.classList.remove('drag-over');

    // Find the closest kanban-cards container in the target column
    var targetColumn = document.getElementById('col-' + newStage);
    var cardsContainer = targetColumn.querySelector('.kanban-cards');

    // Move element in UI
    cardsContainer.appendChild(element);

    // Update Styles immediately
    element.classList.remove('stage-New', 'stage-In-Progress', 'stage-Repaired', 'stage-Scrap');
    // Sanitize newStage string for class name (replace spaces)
    let safeStage = newStage.replace(/\s+/g, '-');
    element.classList.add('stage-' + safeStage);

    // Update Counts
    updateCounts();

    // Call API to update backend
    updateRequestStage(requestId, newStage);
}

async function updateRequestStage(id, stage) {
    let payload = { id: id, stage: stage };


    // If moving to Repaired, we no longer ask for duration
    // if (stage === 'Repaired') { ... }


    try {
        const response = await fetch('/api/requests/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const result = await response.json();
        if (result.success) {
            console.log(`Request ${id} moved to ${stage}`);
            if (stage === 'Scrap') {
                alert("Equipment has been flagged as Scrap!");
            }
        }
    } catch (error) {
        console.error('Error updating request:', error);
    }
}

function updateCounts() {
    document.querySelectorAll('.kanban-column').forEach(col => {
        let count = col.querySelectorAll('.kanban-card').length;
        let countBadge = col.querySelector('.kanban-header .badge');
        if (countBadge) countBadge.innerText = count;
    });
}

// Initial count
window.onload = updateCounts;
