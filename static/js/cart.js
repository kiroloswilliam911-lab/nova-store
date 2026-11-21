document.addEventListener("DOMContentLoaded", function () {
    const cartItems = document.querySelectorAll(".cart-item");

    cartItems.forEach(function (item) {
        item.addEventListener("mouseenter", function () {
            item.style.transform = "translateY(-3px)";
            item.style.transition = "0.3s ease";
        });

        item.addEventListener("mouseleave", function () {
            item.style.transform = "translateY(0)";
        });
    });
});