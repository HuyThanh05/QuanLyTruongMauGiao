nameField = document.getElementById("nameField");
classNameField = document.getElementById("classNameField");
dobField = document.getElementById("dobField");
genderField = document.getElementById("genderField");
parentNameField = document.getElementById("parentNameField");
parentPhoneField = document.getElementById("parentPhoneField");
addressField = document.getElementById("addressField");

weightValue = document.getElementById("weightValue");
heightValue = document.getElementById("heightValue");
tempValue = document.getElementById("tempValue");
currentRecordDate = document.querySelectorAll(".currentRecordDate");


async function fetchKidDataById(useId) {
    const kidsData = await fetchDataUrl(`/api/kids/${useId}`);
    

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

async function fetchHealthRecordById(kidId) {
    const healthRecordData = await fetchDataUrl(`api/health/${kidId}`);

    const healthRecord = healthRecordData.at(-1);

    weightValue.textContent =  healthRecord.weight??"";
    heightValue.textContent =   healthRecord.height??"";
    tempValue.textContent = healthRecord.temperature??"";
    currentRecordDate[0].textContent = healthRecord.date_created??"";
    currentRecordDate[1].textContent = healthRecord.date_created??"";
    currentRecordDate[2].textContent = healthRecord.date_created??"";

    console.log("fetchHealthRecordById called with", kidId);
console.log("healthRecordData =", healthRecordData);
}