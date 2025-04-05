document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".openModal").forEach(button => {
        button.addEventListener("click", function () {
            let imgSrc = this.getAttribute("data-img");
            let modalImage = document.getElementById("modalImage");

            modalImage.setAttribute("src", imgSrc);

            modalImage.classList.remove("animate__zoomIn");
            void modalImage.offsetWidth;
            modalImage.classList.add("animate__zoomIn");

            $("#imageModal").modal("show");
        });
    });

    $("#imageModal").on("hidden.bs.modal", function () {
        document.getElementById("modalImage").classList.remove("animate__zoomIn");
    });
});



const rangeInput = document.getElementById("formControlRange");
const rangeValue = document.getElementById("rangeValue");
const enablePhone = document.getElementById("enablePhone");

enablePhone.addEventListener("change", function () {
    slaiderContainer.style.display = this.checked ? "block" : "none"
});

rangeInput.addEventListener("input", function () {
    let phone = Math.floor(this.value * 100000000).toString();
    phone = phone.padStart(9, "0");
    rangeValue.textContent = "+48 " + phone;
});

$('.carousel').carousel({
    interval: 5000
})

let ctx = document.getElementById("llamaChart").getContext("2d");
let myChart = new Chart(ctx, {
    type: "line",
    data: {
        labels: [
            "Guanaco (Lama guanicoe)",
            "Llama (Lama glama)",
            "Vicuña (Lama vicugna)",
            "Alpaca (Lama pacos)",
        ],
        datasets: [
            {
                label: "Poland",
                data: [0, 2, 0, 3],
                backgroundColor: "rgba(255,100,50,0.6)",
            },
            {
                label: "Argentina",
                data: [7, 10, 8, 6],
                backgroundColor: "rgba(80,100,255,0.6)",
            },
        ],
    },
});
