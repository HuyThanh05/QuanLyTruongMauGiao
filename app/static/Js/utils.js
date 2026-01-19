async function fetchDataUrl(url) {
  const response = await fetch(url, {
    credentials: "same-origin"
  });
  if (!response.ok) {
    console.log("Error fetching:", response.status, url);
    return null;
  }
  return await response.json();
}


function formatNumber(amount) {
  if (amount == null || isNaN(amount)) return "0";
  return new Intl.NumberFormat("en-US", {
    maximumFractionDigits: 0,
  }).format(Number(amount));
}
