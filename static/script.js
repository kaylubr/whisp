document.getElementById('get-link-button').addEventListener('click', function() {
    const linkElement = document.getElementById('unique-link');
    const linkText = linkElement.textContent;

    navigator.clipboard.writeText(linkText).then(() => {
        alert("Link copied to clipboard!");
    }).catch(err => {
        console.error("Could not copy link: ", err);
    });
});