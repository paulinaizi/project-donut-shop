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

    const tiles = modal.querySelectorAll(".option-tile");

    tiles.forEach(tile => {
        tile.addEventListener("click", () => handleTileClick(tile));
    });

    function handleTileClick(tile) {
        const type = tile.dataset.type;
        const id = tile.dataset.id;

        const isSelected =
            (type === "coating" && donutSelection.coating === id) ||
            (type === "sprinkle" && donutSelection.sprinkle === id) ||
            (type === "topCoating" && donutSelection.topCoating === id);

        if (isSelected) {
            if (type === "coating") {
                donutSelection.coating = null;

                donutSelection.sprinkle = null;
            }

            if (type === "sprinkle") {
                donutSelection.sprinkle = null;
            }

            if (type === "topCoating") {
                donutSelection.topCoating = null;
            }

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

        updateUI();
    }

    function randomizeDonut() {

        const coatings = modal.querySelectorAll('.option-tile[data-type="coating"]');
        const sprinkles = modal.querySelectorAll('.option-tile[data-type="sprinkle"]');
        const topCoatings = modal.querySelectorAll('.option-tile[data-type="topCoating"]');

        function pickRandom(tiles) {
            if (!tiles.length) return null;
            const index = Math.floor(Math.random() * tiles.length);
            return tiles[index].dataset.id;
        }

        donutSelection.coating = null;
        donutSelection.sprinkle = null;
        donutSelection.topCoating = null;

        donutSelection.coating = pickRandom(coatings);

        donutSelection.sprinkle = pickRandom(sprinkles);

        donutSelection.topCoating = pickRandom(topCoatings);

        updateUI();
    }

    const randomizeBtn = modal.querySelector(".btn-surprise");
    if (randomizeBtn) {
        randomizeBtn.addEventListener("click", randomizeDonut);
    }

    function resetDonutSelection() {
        donutSelection.coating = null;
        donutSelection.sprinkle = null;
        donutSelection.topCoating = null;

        updateUI();
    }

    modal.addEventListener("hidden.bs.modal", () => {
        resetDonutSelection();
    });

    function updateUI() {
        tiles.forEach(tile => {
            const type = tile.dataset.type;
            const id = tile.dataset.id;

            tile.classList.remove("selected");

            if (type === "coating" && donutSelection.coating === id) {
                tile.classList.add("selected");
            }
            if (type === "sprinkle" && donutSelection.sprinkle === id) {
                tile.classList.add("selected");
            }
            if (type === "topCoating" && donutSelection.topCoating === id) {
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

    updateUI();
};
