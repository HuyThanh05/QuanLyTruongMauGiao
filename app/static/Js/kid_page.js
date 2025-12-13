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

healthRecord1Date = document.getElementById("healthRecord1Date");
healthRecord1Weight = document.getElementById("healthRecord1Weight");
healthRecord1Height = document.getElementById("healthRecord1Height");
healthRecord1Temp = document.getElementById("healthRecord1Temp");
healthRecord1Teacher = document.getElementById("healthRecord1Teacher");
healthRecord1Note = document.getElementById("healthRecord1Note");

healthRecord2Date = document.getElementById("healthRecord2Date");
healthRecord2Weight = document.getElementById("healthRecord2Weight");
healthRecord2Height = document.getElementById("healthRecord2Height");
healthRecord2Temp = document.getElementById("healthRecord2Temp");
healthRecord2Teacher = document.getElementById("healthRecord2Teacher");
healthRecord2Note = document.getElementById("healthRecord2Note");

healthRecord3Date = document.getElementById("healthRecord3Date");
healthRecord3Weight = document.getElementById("healthRecord3Weight");
healthRecord3Height = document.getElementById("healthRecord3Height");
healthRecord3Temp = document.getElementById("healthRecord3Temp");
healthRecord3Teacher = document.getElementById("healthRecord3Teacher");
healthRecord3Note = document.getElementById("healthRecord3Note");

healthRecord4Date = document.getElementById("healthRecord4Date");
healthRecord4Weight = document.getElementById("healthRecord4Weight");
healthRecord4Height = document.getElementById("healthRecord4Height");
healthRecord4Temp = document.getElementById("healthRecord4Temp");
healthRecord4Teacher = document.getElementById("healthRecord4Teacher");
healthRecord4Note = document.getElementById("healthRecord4Note");

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
}


async function fetchHealthHistoryById(kidId) {
    const healthHistoryData = await fetchDataUrl(`api/health/${kidId}`);


    const healthRecord1 = healthHistoryData.at(-1);
    const healthRecord2 = healthHistoryData.at(-2);
    const healthRecord3 = healthHistoryData.at(-3);
    const healthRecord4 = healthHistoryData.at(-4);
    

    healthRecord1Date.textContent = healthRecord1?.date_created??"";
    healthRecord1Weight.textContent = healthRecord1?.weight??"";
    healthRecord1Height.textContent = healthRecord1?.height??"";
    healthRecord1Temp.textContent = healthRecord1?.temperature??"";
    healthRecord1Teacher.textContent = healthRecord1?.teacher.name??"";
    healthRecord1Note.textContent = healthRecord1?.note??"";

    healthRecord2Date.textContent = healthRecord2?.date_created??"";
    healthRecord2Weight.textContent = healthRecord2?.weight??"";
    healthRecord2Height.textContent = healthRecord2?.height??"";
    healthRecord2Temp.textContent = healthRecord2?.temperature??"";
    healthRecord2Teacher.textContent = healthRecord2?.teacher.name??"";
    healthRecord2Note.textContent = healthRecord2?.note??"";

    healthRecord3Date.textContent = healthRecord3?.date_created??"";
    healthRecord3Weight.textContent = healthRecord3?.weight??"";
    healthRecord3Height.textContent = healthRecord3?.height??"";
    healthRecord3Temp.textContent = healthRecord3?.temperature??"";
    healthRecord3Teacher.textContent = healthRecord3?.teacher.name??"";
    healthRecord3Note.textContent = healthRecord3?.note??"";

    healthRecord4Date.textContent = healthRecord4?.date_created??"";
    healthRecord4Weight.textContent = healthRecord4?.weight??"";
    healthRecord4Height.textContent = healthRecord4?.height??"";
    healthRecord4Temp.textContent = healthRecord4?.temperature??"";
    healthRecord4Teacher.textContent = healthRecord4?.teacher.name??"";
    healthRecord4Note.textContent = healthRecord4?.note??"";

    console.log(healthRecord1);



}