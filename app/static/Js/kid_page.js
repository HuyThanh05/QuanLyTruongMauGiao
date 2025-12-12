nameField = document.getElementById("nameField");
classNameField = document.getElementById("classNameField");
dobField = document.getElementById("dobField");
genderField = document.getElementById("genderField");
parentNameField = document.getElementById("parentNameField");
parentPhoneField = document.getElementById("parentPhoneField");
addressField = document.getElementById("addressField");

console.log("kid_page.js loaded");

async function fetchKidDataById(useId) {
    const response = await fetch(`/api/kids/${useId}`);
    const kidsData = await response.json();

    if (!response.ok) {
        console.log("Error fetching kid data:", kidsData.message);
        return;
    }

    const kid = kidsData[0];

    nameField.textContent = kid.name??"";
    classNameField.textContent = kid.class.name??"";
    dobField.textContent = kid.dob??"";
    genderField.textContent = kid.gender??"";
    parentNameField.textContent = kid.parent.name??"";
    parentPhoneField.textContent = kid.parent.phone??"";
    addressField.textContent = kid.address??"";

    console.log(kid);
}