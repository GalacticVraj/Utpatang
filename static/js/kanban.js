function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev, newStage) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    var element = document.getElementById(data);
    var requestId = data.replace('req-', '');

    // Find the closest kanban-cards container in the target column
    var targetColumn = document.getElementById('col-' + newStage);
    var cardsContainer = targetColumn.querySelector('.kanban-cards');

    // Move element in UI
    cardsContainer.appendChild(element);

    // Update Counts
    updateCounts();

    // Call API to update backend
    updateRequestStage(requestId, newStage);
}

async function updateRequestStage(id, stage) {
    let payload = { id: id, stage: stage };

    // If moving to Repaired, ask for duration
    if (stage === 'Repaired') {
        let duration = prompt("Enter hours spent on repair:", "1.0");
        if (duration) payload.actual_duration = parseFloat(duration);
    }

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
