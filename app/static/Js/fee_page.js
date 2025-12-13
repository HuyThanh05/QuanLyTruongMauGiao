console.log("js loaded")
monthly_total_revenue = document.getElementById("monthly-total-revenue");
monthly_collected_ammounts = document.getElementById("monthly-collected-ammounts");
monthly_uncollected_ammounts = document.getElementById("monthly-uncollected-ammounts");

baseFee= document.getElementById("base-fee");
mealFee= document.getElementById("meal-fee");
extraFee = document.getElementById("extra-fee")
totalFee=document.getElementById("total-fee")
paymentStatus = document.getElementById("payment-status")

async function fetchData(){
    totalsData = await fetchDataUrl(`/api/tuitions/totals`);
    console.log(totalsData);

    monthly_total_revenue.textContent = formatNumber(totalsData[0].monthly_revenue);
    monthly_collected_ammounts.textContent = formatNumber(totalsData[0].monthly_collected_amounts);
    monthly_uncollected_ammounts.textContent = formatNumber(totalsData[0].monthly_uncollected_amounts);

    //xử lý học phí của học sinh
    tuitionsFee = await fetchDataUrl(`/api/tuitions`);
    console.log(tuitionsFee);

    const tbody = document.querySelector(".tuition-body");
    console.log(tbody);

    for (let tuition of tuitionsFee){
        const row = document.createElement("tr");
        console.log(row);

        let statusClass = "text-bg-secondary";
        if(tuition.status === "Paid"){
            statusClass = "text-bg-success";
        }
        else{
            statusClass="text-bg-danger";
        }

        row.innerHTML = `
            <td>${tuition.student.name}</td>
              <td class="text-end" >${formatNumber(tuition.fee_base)}</td>
              <td class="text-end" >${formatNumber(tuition.meal_fee)}</td>
              <td class="text-end" >${formatNumber(tuition.extra_fee)}</td>
              <td class="text-end fw-semibold" id="total-fee">${formatNumber(tuition.fee_base+tuition.meal_fee+tuition.extra_fee)}</td>
              <td class="text-center">
                <span class="badge ${statusClass}" id="payment-status"
                  >${tuition.status === "Paid"? "Đã thu" : "Chưa thu"}</span
                >
              </td>
              <td class="text-end">05/12/2025</td>
        `;
        tbody.appendChild(row);
    }
}