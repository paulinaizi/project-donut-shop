const modal = document.getElementById("donutCreatorModal");

let donutInitialized = false;

modal.addEventListener("shown.bs.modal", () => {
    if (donutInitialized) return;

    initDonutCreator();
    donutInitialized = true;
});

function initDonutCreator() {

    const donutSelection = {
        coating: null,
        sprinkle: null,
        topCoating: null
    };

    function isDonutEmpty() {
        return (
            donutSelection.coating === null &&
            donutSelection.sprinkle === null &&
            donutSelection.topCoating === null
        );
    }

    const addToCartButton = modal.querySelector(".add-to-cart");

    function syncCartButton() {
        addToCartButton.dataset.toppings = JSON.stringify(donutSelection);

        if (isDonutEmpty()) {
            addToCartButton.disabled = true;
            addToCartButton.classList.add("disabled");
        } else {
            addToCartButton.disabled = false;
            addToCartButton.classList.remove("disabled");
        }
    }

    const tiles = modal.querySelectorAll(".option-tile");

    tiles.forEach(tile => {
        tile.addEventListener("click", () => handleTileClick(tile));
    });

    function handleTileClick(tile) {
        const {
            type,
            id
        } = tile.dataset;

        const isSelected = donutSelection[type] === id;

        if (isSelected) {
            donutSelection[type] = null;

            if (type === "coating") {
                donutSelection.sprinkle = null;
            }

            syncCartButton();
            updateUI();
            return;
        }

        if (type === "coating") {
            donutSelection.coating = id;
        }

        if (type === "sprinkle") {
            if (!donutSelection.coating) {
                alert("Najpierw wybierz polewę - posypka się nie przyklei! :)");
                return;
            }
            donutSelection.sprinkle = id;
        }

        if (type === "topCoating") {
            donutSelection.topCoating = id;
        }

        syncCartButton();
        updateUI();
    }

    function randomizeDonut() {

        const types = ["coating", "sprinkle", "topCoating"];

        types.forEach(type => {
            const tiles = modal.querySelectorAll(`.option-tile[data-type="${type}"]`)
            donutSelection[type] = pickRandomId(tiles);
        });

        syncCartButton();
        updateUI();

    }

    function pickRandomId(tiles){
        if (!tiles.length) return null;
        const index = Math.floor(Math.random() * tiles.length);
        return tiles[index].dataset.id;
    }

    const randomizeBtn = modal.querySelector(".btn-surprise");
    if (randomizeBtn) {
        randomizeBtn.addEventListener("click", randomizeDonut);
    }

    function resetDonutSelection() {
        donutSelection.coating = null;
        donutSelection.sprinkle = null;
        donutSelection.topCoating = null;

        syncCartButton();
        updateUI();
    }

    modal.addEventListener("hidden.bs.modal", () => {
        resetDonutSelection();
    });

    function updateUI() {
        tiles.forEach(tile => {
            const { 
                type, 
                id 
            } = tile.dataset;

            tile.classList.remove("selected");

            if (donutSelection[type] === id) {
                tile.classList.add("selected");
            }
        });

        modal.querySelectorAll('.option-tile[data-type="sprinkle"]').forEach(tile => {
            if (!donutSelection.coating) {
                tile.classList.add("disabled");
            } else {
                tile.classList.remove("disabled");
            }
        });
    }

    syncCartButton();
    updateUI();
};