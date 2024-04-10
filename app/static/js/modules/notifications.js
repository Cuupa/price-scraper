export function showSuccessPopup(title, message) {
    Swal.fire({
        position: "top-end",
        icon: "success",
        title: title,
        text: message,
        showConfirmButton: false,
        timer: 2500,
        width: 300
    });
}

export function showErrorPopup(title, message) {
    Swal.fire({
        position: "top-end",
        icon: "error",
        title: title,
        text: message,
        showConfirmButton: false,
        timer: 2500,
        width: 300
    });
}