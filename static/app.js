document.addEventListener("DOMContentLoaded", () => {
    const turniList = document.getElementById("turni-list");
    const formAddTurno = document.getElementById("form-add-turno");
    const modalAddTurno = new bootstrap.Modal(document.getElementById("modal-add-turno"));

    // Mostra messaggi di errore o successo
    const showMessage = (message, type = "success") => {
        const feedback = document.createElement("div");
        feedback.className = `alert alert-${type} alert-dismissible fade show`;
        feedback.textContent = message;
        feedback.innerHTML += `
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        document.body.appendChild(feedback);

        setTimeout(() => {
            if (feedback) feedback.remove();
        }, 5000);
    };

    // Mostra loader nella tabella
    const showLoader = () => {
        turniList.innerHTML = '<tr><td colspan="5" class="text-center">Caricamento in corso...</td></tr>';
    };

    // Carica i turni
    const loadTurni = async () => {
        showLoader();
        try {
            const response = await fetch("/turni");
            if (!response.ok) throw new Error("Errore durante il caricamento dei turni.");

            const turni = await response.json();
            turniList.innerHTML = ""; // Svuota la tabella

            turni.forEach(turno => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${turno.data}</td>
                    <td>${turno.orario_inizio}</td>
                    <td>${turno.orario_fine}</td>
                    <td>${turno.note || ""}</td>
                    <td>
                        <button class="btn btn-danger btn-sm btn-delete" data-id="${turno.id}">Elimina</button>
                    </td>
                `;
                turniList.appendChild(row);
            });
        } catch (error) {
            console.error("Errore durante il caricamento dei turni:", error);
            turniList.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Errore nel caricamento.</td></tr>';
        }
    };

    // Aggiungi un turno
    formAddTurno.addEventListener("submit", async (e) => {
        e.preventDefault(); // Previeni il comportamento predefinito

        const turno = {
            data: document.getElementById("data").value,
            orario_inizio: document.getElementById("orario-inizio").value,
            orario_fine: document.getElementById("orario-fine").value,
            note: document.getElementById("note").value,
        };

        // Validazione dati
        if (new Date(`${turno.data}T${turno.orario_fine}`) <= new Date(`${turno.data}T${turno.orario_inizio}`)) {
            showMessage("L'orario di fine deve essere successivo all'orario di inizio.", "danger");
            return;
        }

        try {
            const response = await fetch("/turni", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(turno),
            });

            if (!response.ok) throw new Error("Errore durante l'aggiunta del turno.");

            showMessage("Turno aggiunto con successo!");
            modalAddTurno.hide();
            formAddTurno.reset(); // Resetta il form
            loadTurni(); // Ricarica la lista
        } catch (error) {
            console.error("Errore durante l'aggiunta del turno:", error);
            showMessage("Errore durante l'aggiunta del turno. Riprova più tardi.", "danger");
        }
    });

    // Delegazione per il pulsante elimina
    turniList.addEventListener("click", async (e) => {
        if (e.target.classList.contains("btn-delete")) {
            const id = e.target.getAttribute("data-id");
            if (confirm("Sei sicuro di voler eliminare questo turno?")) {
                try {
                    const response = await fetch(`/turni/${id}`, {
                        method: "DELETE",
                    });

                    if (!response.ok) throw new Error("Errore durante l'eliminazione del turno.");

                    showMessage("Turno eliminato con successo!");
                    loadTurni(); // Ricarica la lista
                } catch (error) {
                    console.error("Errore durante l'eliminazione del turno:", error);
                    showMessage("Errore durante l'eliminazione del turno. Riprova più tardi.", "danger");
                }
            }
        }
    });

    // Inizializza la lista dei turni
    loadTurni();
});
