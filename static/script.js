document.addEventListener("DOMContentLoaded", () => {
    // Form navigation elements
    const form = document.getElementById("predictionForm");
    const steps = document.querySelectorAll(".form-step");
    const stepItems = document.querySelectorAll(".step-item");
    const progressBarFill = document.getElementById("progressBarFill");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    
    // Screens
    const loadingOverlay = document.getElementById("loadingOverlay");
    const resultsContainer = document.getElementById("resultsContainer");
    
    let currentStep = 1;
    const totalSteps = steps.length;

    // Linked Inputs definitions (Slider <-> Number Box)
    const linkedInputs = [
        { slider: "heightSlider", number: "heightNum" },
        { slider: "weightSlider", number: "weightNum" },
        { slider: "cholesterolSlider", number: "cholesterolNum" },
        { slider: "glucoseSlider", number: "glucoseNum" },
        { slider: "boneSlider", number: "boneNum" },
        { slider: "visionSlider", number: "visionNum" },
        { slider: "hearingSlider", number: "hearingNum" },
        { slider: "stressSlider", number: "stressNum" },
        { slider: "cognitiveSlider", number: "cognitiveNum" },
        { slider: "pollutionSlider", number: "pollutionNum" },
        { slider: "sunSlider", number: "sunNum" }
    ];

    // Initialize Linked Inputs
    linkedInputs.forEach(pair => {
        const sliderEl = document.getElementById(pair.slider);
        const numberEl = document.getElementById(pair.number);

        if (sliderEl && numberEl) {
            // Slider changes -> Number updates
            sliderEl.addEventListener("input", (e) => {
                numberEl.value = e.target.value;
                if (pair.slider === "heightSlider" || pair.slider === "weightSlider") {
                    calculateBMI();
                }
            });

            // Number changes -> Slider updates
            numberEl.addEventListener("input", (e) => {
                let val = parseFloat(e.target.value);
                const min = parseFloat(sliderEl.min);
                const max = parseFloat(sliderEl.max);

                if (isNaN(val)) return;
                
                // Clamp value for slider safety
                if (val < min) val = min;
                if (val > max) val = max;

                sliderEl.value = val;
                
                if (pair.slider === "heightSlider" || pair.slider === "weightSlider") {
                    calculateBMI();
                }
            });
        }
    });

    // Real-time BMI Calculation
    function calculateBMI() {
        const height = parseFloat(document.getElementById("heightNum").value);
        const weight = parseFloat(document.getElementById("weightNum").value);
        const bmiEl = document.getElementById("bmi");
        const bmiIndicator = document.getElementById("bmiIndicator");

        if (height > 0 && weight > 0) {
            const heightInMeters = height / 100;
            const bmi = weight / (heightInMeters * heightInMeters);
            const formattedBmi = bmi.toFixed(1);
            
            bmiEl.value = formattedBmi;

            // Update badge classification
            bmiIndicator.className = "bmi-indicator"; // Reset
            if (bmi < 18.5) {
                bmiIndicator.classList.add("underweight");
                bmiIndicator.textContent = "Underweight";
            } else if (bmi < 25.0) {
                bmiIndicator.classList.add("normal");
                bmiIndicator.textContent = "Normal Weight";
            } else if (bmi < 30.0) {
                bmiIndicator.classList.add("overweight");
                bmiIndicator.textContent = "Overweight";
            } else {
                bmiIndicator.classList.add("obese");
                bmiIndicator.textContent = "Obese";
            }
        }
    }

    // Initial BMI calculation
    calculateBMI();

    // Step Navigation logic
    function updateWizard() {
        // Show/Hide steps
        steps.forEach((step, idx) => {
            if (idx + 1 === currentStep) {
                step.classList.add("active");
            } else {
                step.classList.remove("active");
            }
        });

        // Update step status in header
        stepItems.forEach((item, idx) => {
            const stepNum = idx + 1;
            item.className = "step-item"; // Reset classes
            
            if (stepNum === currentStep) {
                item.classList.add("active");
            } else if (stepNum < currentStep) {
                item.classList.add("completed");
            }
        });

        // Update progress bar fill
        const progressPercent = ((currentStep - 1) / (totalSteps - 1)) * 100;
        progressBarFill.style.width = `${progressPercent}%`;

        // Update navigation button states
        prevBtn.disabled = currentStep === 1;
        
        if (currentStep === totalSteps) {
            nextBtn.textContent = "Analyze Biological Age 🔍";
            nextBtn.classList.remove("btn-primary");
            nextBtn.classList.add("btn-primary"); // Can style differently if needed
        } else {
            nextBtn.textContent = "Continue";
        }
    }

    // Next / Submit Button
    nextBtn.addEventListener("click", () => {
        // Simple step validation (check required inputs in current step)
        const activeStepEl = document.getElementById(`step${currentStep}`);
        const requiredInputs = activeStepEl.querySelectorAll("[required]");
        let isValid = true;

        requiredInputs.forEach(input => {
            if (!input.value.trim()) {
                input.reportValidity();
                isValid = false;
            }
        });

        if (!isValid) return;

        if (currentStep < totalSteps) {
            currentStep++;
            updateWizard();
        } else {
            submitForm();
        }
    });

    // Prev Button
    prevBtn.addEventListener("click", () => {
        if (currentStep > 1) {
            currentStep--;
            updateWizard();
        }
    });

    // Stepper item clicks (only allow navigation to current or previously completed steps)
    stepItems.forEach(item => {
        item.addEventListener("click", () => {
            const targetStep = parseInt(item.getAttribute("data-step"));
            if (targetStep < currentStep || item.classList.contains("completed") || targetStep === currentStep) {
                currentStep = targetStep;
                updateWizard();
            }
        });
    });

    // Collect all inputs and submit
    async function submitForm() {
        loadingOverlay.classList.add("active");
        
        // Gather data
        const formData = {};

        // 1. Numerical Slider Inputs
        linkedInputs.forEach(pair => {
            const numEl = document.getElementById(pair.number);
            const keyName = getApiKeyName(pair.number);
            formData[keyName] = parseFloat(numEl.value);
        });

        // 2. Selects & Radio / Segment buttons
        formData["Gender"] = document.querySelector('input[name="Gender"]:checked').value;
        formData["Physical Activity Level"] = document.querySelector('input[name="Physical Activity Level"]:checked').value;
        formData["Smoking Status"] = document.querySelector('input[name="Smoking Status"]:checked').value;
        formData["Alcohol Consumption"] = document.querySelector('input[name="Alcohol Consumption"]:checked').value;
        formData["Diet"] = document.querySelector('input[name="Diet"]:checked').value;
        formData["Sleep Patterns"] = document.querySelector('input[name="Sleep Patterns"]:checked').value;
        formData["Mental Health Status"] = document.querySelector('input[name="Mental Health Status"]:checked').value;
        formData["Income Level"] = document.querySelector('input[name="Income Level"]:checked').value;
        
        formData["Chronic Diseases"] = document.getElementById("chronic").value;
        formData["Medication Use"] = document.getElementById("medication").value;
        formData["Family History"] = document.getElementById("family").value;
        formData["Education Level"] = document.getElementById("education").value;

        // Auto-calculated fields
        formData["BMI"] = parseFloat(document.getElementById("bmi").value);

        // Blood pressure combination
        const sys = document.getElementById("bpSystolic").value;
        const dia = document.getElementById("bpDiastolic").value;
        formData["Blood Pressure (s/d)"] = `${sys}/${dia}`;

        // Get Chronological age for comparison display
        const chronologicalAge = parseFloat(document.getElementById("actualAge").value);

        try {
            const response = await fetch("/api/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();
            
            if (result.success) {
                setTimeout(() => {
                    displayResults(result, chronologicalAge);
                }, 1000); // Small delay to feel more thorough and show animations
            } else {
                alert("Error calling predictor API: " + result.error);
                loadingOverlay.classList.remove("active");
            }
        } catch (err) {
            alert("Network error: " + err.message);
            loadingOverlay.classList.remove("active");
        }
    }

    // Map UI element IDs to API feature name keys
    function getApiKeyName(id) {
        switch(id) {
            case "heightNum": return "Height (cm)";
            case "weightNum": return "Weight (kg)";
            case "cholesterolNum": return "Cholesterol Level (mg/dL)";
            case "glucoseNum": return "Blood Glucose Level (mg/dL)";
            case "boneNum": return "Bone Density (g/cm²)";
            case "visionNum": return "Vision Sharpness";
            case "hearingNum": return "Hearing Ability (dB)";
            case "stressNum": return "Stress Levels";
            case "cognitiveNum": return "Cognitive Function";
            case "pollutionNum": return "Pollution Exposure";
            case "sunNum": return "Sun Exposure";
            default: return id;
        }
    }

    // Display Results & Animate Gauge
    function displayResults(data, chronologicalAge) {
        loadingOverlay.classList.remove("active");
        form.style.display = "none";
        document.querySelector(".progress-container").style.display = "none";
        resultsContainer.classList.add("active");

        const predictedAge = data.predicted_age;
        
        // 1. Text updates
        document.getElementById("predictedAgeVal").textContent = predictedAge.toFixed(2);
        document.getElementById("chronoAgeVal").textContent = chronologicalAge;
        document.getElementById("bioAgeVal").textContent = predictedAge.toFixed(1);

        // 2. Risk badge styling
        const riskBadge = document.getElementById("riskBadge");
        riskBadge.textContent = data.status;
        riskBadge.className = "status-badge"; // Reset classes
        if (data.status === "Optimal") {
            riskBadge.classList.add("optimal");
        } else if (data.status === "Moderate") {
            riskBadge.classList.add("moderate");
        } else {
            riskBadge.classList.add("high-risk");
        }

        // 3. Comparison text card
        const compSummary = document.getElementById("comparisonSummary");
        compSummary.className = "comparison-summary"; // Reset
        const difference = predictedAge - chronologicalAge;

        if (difference < -1.5) {
            compSummary.classList.add("younger");
            compSummary.innerHTML = `Your biological age is <strong style="color:var(--color-green);">${Math.abs(difference).toFixed(1)} years younger</strong> than your actual chronological age! Your healthy choices are helping you slow down biological aging.`;
        } else if (difference > 1.5) {
            compSummary.classList.add("older");
            compSummary.innerHTML = `Your biological age is <strong style="color:var(--color-red);">${difference.toFixed(1)} years older</strong> than your actual chronological age. Review the insights below to target areas of improvement.`;
        } else {
            compSummary.classList.add("same");
            compSummary.innerHTML = `Your biological age is aligned with your actual chronological age (difference of <strong>${difference.toFixed(1)} years</strong>). Maintain healthy lifestyle habits to remain vital.`;
        }

        // 4. Animate Gauge & Needle
        // Map predicted age (18 to 90 years) to gauge (dashoffset: 251.2 to 0, angle: -90 to +90 deg)
        const minAge = 18;
        const maxAge = 90;
        let percentage = (predictedAge - minAge) / (maxAge - minAge);
        percentage = Math.max(0, Math.min(1, percentage)); // Clamp between 0 and 1

        const dashoffset = 251.2 - (percentage * 251.2);
        const rotationAngle = -90 + (percentage * 180);

        // Set attributes dynamically (which triggers CSS transitions)
        setTimeout(() => {
            const gaugeFill = document.getElementById("gaugeFill");
            const gaugeNeedle = document.getElementById("gaugeNeedle");
            
            gaugeFill.style.strokeDashoffset = dashoffset;
            gaugeNeedle.style.transform = `rotate(${rotationAngle}deg)`;
        }, 100);

        // 5. Fill Health Recommendations / Tips
        const tipsGrid = document.getElementById("tipsGrid");
        tipsGrid.innerHTML = ""; // Clear

        data.tips.forEach(tip => {
            const card = document.createElement("div");
            card.className = "tip-card";
            
            card.innerHTML = `
                <div class="tip-icon">${tip.icon}</div>
                <div class="tip-content">
                    <div class="tip-header">
                        <span class="tip-category">${tip.category}</span>
                        <span class="tip-impact ${tip.impact.toLowerCase()}">${tip.impact} Impact</span>
                    </div>
                    <p class="tip-text">${tip.text}</p>
                </div>
            `;
            
            tipsGrid.appendChild(card);
        });
    }

    // Retest Button - reset everything back to form step 1
    const retestBtn = document.getElementById("retestBtn");
    retestBtn.addEventListener("click", () => {
        resultsContainer.classList.remove("active");
        form.style.display = "block";
        document.querySelector(".progress-container").style.display = "block";
        
        // Reset gauge
        document.getElementById("gaugeFill").style.strokeDashoffset = "251.2";
        document.getElementById("gaugeNeedle").style.transform = "rotate(-90deg)";

        currentStep = 1;
        updateWizard();
    });
});
