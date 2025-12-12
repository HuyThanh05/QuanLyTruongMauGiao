async function fetchDataUrl(url) {
    const response = await fetch(url);
    if (!response.ok) {
        console.log("Error fetching:");
        return;
    }
    return await response.json();
}