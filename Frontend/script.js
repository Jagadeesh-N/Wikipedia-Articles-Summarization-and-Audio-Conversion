document.addEventListener("DOMContentLoaded", function() {
    const welcomeMessage = document.getElementById("welcomeMessage");
    const contentContainer = document.getElementById("contentContainer");

    console.log("Initializing application...");

    // Hide the welcome message and show the content after 2 seconds
    setTimeout(() => {
        console.log("Hiding welcome message and showing main content.");
        welcomeMessage.style.display = "none";
        contentContainer.style.display = "flex";
    }, 2000);

    // Clear input fields on load
    document.getElementById("articleInput").value = "";
    document.getElementById("summaryLength").value = "";

    // Initialize audio player controls
    initializeAudioPlayer();
});

// To store the metadata for the current session
let currentMetadata = null;

// Helper function to format time
function formatTime(seconds) {
    if (isNaN(seconds)) return "0:00";
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
}

// Function to initialize audio player controls
function initializeAudioPlayer() {
    console.log("Initializing audio player controls...");
    const audio = document.getElementById("audioPlayer");
    const playPauseBtn = document.getElementById("playPauseBtn");
    const seekSlider = document.getElementById("seekSlider");
    const volumeSlider = document.getElementById("volumeSlider");
    const muteBtn = document.getElementById("muteBtn");
    const speedSelect = document.getElementById("playbackSpeed");
    const currentTimeSpan = document.getElementById("currentTime");
    const durationSpan = document.getElementById("duration");

    // Play/Pause functionality
    playPauseBtn.addEventListener("click", () => {
        if (audio.paused) {
            console.log("Playing audio...");
            audio.play();
            playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
        } else {
            console.log("Pausing audio...");
            audio.pause();
            playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
        }
    });

    // Update seek slider and time display
    audio.addEventListener("timeupdate", () => {
        if (!isNaN(audio.duration)) {
            const percent = (audio.currentTime / audio.duration) * 100;
            seekSlider.value = percent;
            currentTimeSpan.textContent = formatTime(audio.currentTime);
        }
    });

    // Seek functionality
    seekSlider.addEventListener("input", () => {
        const time = (seekSlider.value / 100) * audio.duration;
        console.log(`Seeking to time: ${time}s`);
        audio.currentTime = time;
    });

    // Volume control
    volumeSlider.addEventListener("input", () => {
        audio.volume = volumeSlider.value;
        console.log(`Volume changed to: ${audio.volume}`);
        updateVolumeIcon();
    });

    // Mute toggle
    muteBtn.addEventListener("click", () => {
        audio.muted = !audio.muted;
        console.log(`Audio muted: ${audio.muted}`);
        updateVolumeIcon();
    });

    // Playback speed control
    speedSelect.addEventListener("change", () => {
        audio.playbackRate = speedSelect.value;
        console.log(`Playback speed set to: ${audio.playbackRate}`);
    });

    // Update duration when metadata is loaded
    audio.addEventListener("loadedmetadata", () => {
        seekSlider.max = 100;
        durationSpan.textContent = formatTime(audio.duration);
        currentTimeSpan.textContent = "0:00";
        console.log(`Audio duration: ${audio.duration}s`);
    });

    // Ensure duration updates on audio load
    audio.addEventListener("canplaythrough", () => {
        durationSpan.textContent = formatTime(audio.duration || 0);
        console.log("Audio can be played through.");
    });

    // Helper function to update volume icon
    function updateVolumeIcon() {
        const icon = muteBtn.querySelector("i");
        if (audio.muted || audio.volume === 0) {
            icon.className = "fas fa-volume-mute";
        } else if (audio.volume < 0.5) {
            icon.className = "fas fa-volume-down";
        } else {
            icon.className = "fas fa-volume-up";
        }
    }
}

// Function to submit the request
async function submitRequest() {
    const articleInput = document.getElementById("articleInput").value;
    const summaryLength = document.getElementById("summaryLength").value;
    const form = document.getElementById("wikiForm");
    const responseDiv = document.getElementById("response");
    const loadingIndicator = document.getElementById("loadingIndicator");
    const requestSummary = document.getElementById("requestSummary");

    console.log("Submitting request...");

    // Input validation
    if (!articleInput || !summaryLength) {
        alert("Please fill in both fields.");
        console.error("Validation failed: Missing input fields.");
        return;
    }

    console.log(`Article Input: ${articleInput}`);
    console.log(`Summary Length: ${summaryLength}`);

    // Update request summary in loading state
    requestSummary.innerHTML = `
        <div>Wikipedia URL: ${articleInput}</div>
        <div>Target Length: ${summaryLength} words</div>
    `;

    // Hide form and show loading indicator
    form.style.display = "none";
    loadingIndicator.style.display = "flex";
    responseDiv.style.display = "none";

    const requestData = {
        input: articleInput,
        target_length: parseInt(summaryLength),
    };

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 300000); // Set 5-minute timeout
    try {
        console.log("Sending request to backend...");
        const response = await fetch("http://34.8.204.138/process", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestData),
            signal: controller.signal, // Attach the signal for aborting
            credentials: "include" // Include credentials if necessary
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const result = await response.json();

        // Store metadata for rating submission
        currentMetadata = result.metadata;
        console.log("Received metadata:", currentMetadata);

        // Update response section with summary and audio
        document.getElementById("summaryText").textContent = result.summary;
        const audioPlayer = document.getElementById("audioPlayer");
        audioPlayer.src = `data:audio/mp3;base64,${result.audio_base64}`;
        document.getElementById("downloadLink").href = `data:audio/mp3;base64,${result.audio_base64}`;
		// Reset audio player controls
        const playPauseBtn = document.getElementById("playPauseBtn");
        const seekSlider = document.getElementById("seekSlider");
        const currentTimeSpan = document.getElementById("currentTime");
        const durationSpan = document.getElementById("duration");

        playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
        seekSlider.value = 0;
        currentTimeSpan.textContent = "0:00";

        // Ensure accurate duration is displayed
        audioPlayer.addEventListener("loadedmetadata", () => {
            durationSpan.textContent = formatTime(audioPlayer.duration || 0);
        });
        responseDiv.style.display = "flex";

        console.log("Request processed successfully.");
    } catch (error) {
        if (error.name === "AbortError") {
            console.error("Request timed out.");
            responseDiv.innerHTML = `<p>Error: Request timed out.</p>`;
        } else {
            console.error("Error:", error.message);
            responseDiv.innerHTML = `<p>Error: ${error.message}</p>`;
        }
        responseDiv.style.display = "block";
    } finally {
        clearTimeout(timeoutId);
        loadingIndicator.style.display = "none";
    }
}

// Function to submit the user's rating
async function submitRating() {
    const rating = document.getElementById("userRating").value;
    const tryAgainButton = document.getElementById("tryAgainButton");

    if (!currentMetadata) {
        alert("No metadata available. Please process an article first.");
        console.error("No metadata available for submitting rating.");
        return;
    }

    if (!rating || rating < 0 || rating > 10) {
        alert("Please enter a valid rating between 0 and 10.");
        console.error("Invalid rating input.");
        return;
    }

    const ratingPayload = {
        ...currentMetadata,
        user_rating: parseInt(rating),
    };

    console.log("Submitting rating:", ratingPayload);

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 300000); // Set 5-minute timeout

    try {
        const response = await fetch("http://34.8.204.138/submit_rating", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(ratingPayload),
            signal: controller.signal, // Attach the signal for aborting
            credentials: "include" // Include credentials if necessary
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const result = await response.json();
        alert(result.message);
        console.log("Rating submitted successfully:", result.message);

        // Show "Try Again" button and hide submit button
        tryAgainButton.style.display = "block";
    } catch (error) {
        if (error.name === "AbortError") {
            alert("Error: Request timed out.");
            console.error("Rating submission request timed out.");
        } else {
            alert(`Error submitting rating: ${error.message}`);
            console.error("Error submitting rating:", error.message);
        }
    } finally {
        clearTimeout(timeoutId);
    }
}

// Function to handle "Try Again" logic
function tryAgain() {
    console.log("Resetting form for a new attempt")
    const responseDiv = document.getElementById("response");
    const wikiForm = document.getElementById("wikiForm");
    const articleInput = document.getElementById("articleInput");
    const summaryLength = document.getElementById("summaryLength");
    const userRating = document.getElementById("userRating");
    const tryAgainButton = document.getElementById("tryAgainButton");

    // Reset fields
    responseDiv.style.display = "none";
    wikiForm.style.display = "flex";
    contentContainer.style.display = "flex";
    articleInput.value = "";
    summaryLength.value = "";
    userRating.value = "";
    currentMetadata = null;
    tryAgainButton.style.display = "none";
}