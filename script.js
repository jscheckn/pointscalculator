document.getElementById("convert-btn").addEventListener("click", async function() {
    const raceTimeInput = document.getElementById("race-time").value;
    const ageGroup = document.getElementById("age-group").value;
    const event = document.getElementById("event").value;
    const gender = document.getElementById("gender").value;
    const resultDiv = document.getElementById("result");
    
    let inputEntry = [gender, ageGroup, event].join("-")
    // Database of times by age group and gender

    let timeDatabase;
    try {
        const response = await fetch("data/Times.json"); // Adjust path as needed
        if (!response.ok) throw new Error("Failed to load time database.");
        timeDatabase = await response.json();
    } catch (error) {
        resultDiv.textContent = "Error loading time database.";
        console.error(error);
        return;
    }

    // Clear previous result
    resultDiv.textContent = "";

    // Validate input format (mm:ss.SS)
    const timePattern = /^\d{1,2}:\d{2}\.\d{2}$/;
    const otherTimePattern = /^\d{1,2}\.\d{2}$/
    if (!timePattern.test(raceTimeInput) && !otherTimePattern.test(raceTimeInput)) {
        resultDiv.textContent = "Please enter a valid time in mm:ss.SS format.";
        return;
    }
    let format = "";
    if(!timePattern.test(raceTimeInput)){
        format = "seconds";
    }else{
        format = "mins";
    }

    // Validate age group and gender selection
    if (!timeDatabase[inputEntry]) {
        resultDiv.textContent = "Invalid age group or gender selected.";
        return;
    }
    let totalSeconds = 0;
    // Parse minutes, seconds, and centiseconds
    if(format == "mins"){
        const [minutes, secondsAndCentiseconds] = raceTimeInput.split(":");
        const [seconds, centiseconds] = secondsAndCentiseconds.split(".").map(Number);
        totalSeconds = (minutes * 60 + seconds) + centiseconds*0.01
        
    }else{
        const [seconds, centiseconds] = raceTimeInput.split(".").map(Number);
        totalSeconds = seconds + centiseconds*0.01
    }



    // Retrieve reference time from database
    let baseTime = timeDatabase[inputEntry]["Time"];
    if(!timePattern.test(baseTime)){
        format = "seconds";
    }else{
        format = "mins";
    }

    if(isNaN(baseTime/1)){
        let [m, sc] = baseTime.split(":");
        m = m.slice(1);
        const [s, c] = sc.split(".").map(Number);
        baseTime = (m * 60 + s) + c*0.01
        
    }

    const points = (1000 * Math.pow((baseTime/totalSeconds), 3)).toFixed(0);

    // Calculate point total as a percentage of the reference time

    if(baseTime == ""){
        resultDiv.textContent = `Points cannot be calculated with these selections. Try again with a different selection`
    }else if(points > 1100){
        resultDiv.textContent = `Input time cannot be calculated. Try again with a different time.`
    }else{
        resultDiv.textContent = `The points conversion for your time is ${points}.`
    }
    
});
