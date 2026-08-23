const button = document.getElementById("micButton");
const responseBox = document.getElementById("response");

let recognition = null;

let isListening = false;


// ==================================================
// CHECK ELEMENTS
// ==================================================

if (!button) {

    console.error("ERROR: micButton not found.");

}

if (!responseBox) {

    console.error("ERROR: response element not found.");

}


// ==================================================
// SPEECH RECOGNITION
// ==================================================

if ("webkitSpeechRecognition" in window) {

    recognition = new webkitSpeechRecognition();

    recognition.continuous = false;

    recognition.interimResults = false;

    recognition.lang = "en-IN";


    // ==================================================
    // MICROPHONE STARTED
    // ==================================================

    recognition.onstart = function () {

        console.log("Microphone started.");

        isListening = true;

        button.disabled = true;

        button.innerText =
            "🎙️ Listening... Speak now";

        responseBox.innerText =
            "I'm listening... Speak now.";

    };


    // ==================================================
    // SPEECH RESULT
    // ==================================================

    recognition.onresult = async function (event) {

        const userText =
            event.results[0][0].transcript;

        console.log(
            "User said:",
            userText
        );


        responseBox.innerText =
            "You: " + userText;


        button.innerText =
            "🤔 Thinking...";


        try {

            // ==========================================
            // SEND REQUEST TO BACKEND
            // ==========================================

            const url =
                "http://127.0.0.1:8000/coach?message=" +
                encodeURIComponent(userText);


            console.log(
                "Sending request:",
                url
            );


            const result =
                await fetch(url);


            console.log(
                "Backend status:",
                result.status
            );


            if (!result.ok) {

                throw new Error(
                    "Backend returned HTTP " +
                    result.status
                );

            }


            // ==========================================
            // GET AI RESPONSE
            // ==========================================

            const data =
                await result.json();


            console.log(
                "AI response:",
                data
            );


            // ==========================================
            // SHOW AI RESPONSE
            // ==========================================

            responseBox.innerText =
                "Coach: " +
                data.coach_response;


            // ==========================================
            // PLAY RIME AUDIO
            // ==========================================

            const audio =
                new Audio(
                    "http://127.0.0.1:8000/audio"
                );


            audio.play()
                .then(function () {

                    console.log(
                        "Rime audio playing."
                    );

                })
                .catch(function (error) {

                    console.warn(
                        "Audio autoplay blocked:",
                        error
                    );

                    // DON'T SHOW "Something went wrong"
                    // because AI response itself worked.

                });


        }

        catch (error) {

            console.error(
                "Frontend / Backend error:",
                error
            );


            responseBox.innerText =
                "Something went wrong.\n\n" +
                "Check the browser console.";

        }


        // ==========================================
        // RESET BUTTON
        // ==========================================

        button.disabled = false;

        button.innerText =
            "🎙️ Talk to Coach";

        isListening = false;

    };


    // ==================================================
    // SPEECH ERROR
    // ==================================================

    recognition.onerror = function (event) {

        console.error(
            "Speech recognition error:",
            event.error
        );


        if (event.error === "no-speech") {

            responseBox.innerText =
                "I couldn't hear you.\n\n" +
                "Please speak clearly and try again.";

        }

        else if (event.error === "not-allowed") {

            responseBox.innerText =
                "Microphone permission was denied.\n\n" +
                "Please allow microphone access.";

        }

        else if (event.error === "aborted") {

            responseBox.innerText =
                "Listening stopped.\n\n" +
                "Try again.";

        }

        else {

            responseBox.innerText =
                "Microphone error: " +
                event.error;

        }


        button.disabled = false;

        button.innerText =
            "🎙️ Talk to Coach";

        isListening = false;

    };


    // ==================================================
    // SPEECH ENDED
    // ==================================================

    recognition.onend = function () {

        console.log(
            "Microphone stopped."
        );


        isListening = false;


        if (
            button.innerText ===
            "🎙️ Listening... Speak now"
        ) {

            button.disabled = false;

            button.innerText =
                "🎙️ Talk to Coach";

        }

    };

}


// ==================================================
// SPEECH RECOGNITION NOT SUPPORTED
// ==================================================

else {

    console.error(
        "Speech recognition not supported."
    );


    responseBox.innerText =
        "Speech recognition is not supported in this browser.";

}


// ==================================================
// MICROPHONE BUTTON
// ==================================================

button.addEventListener(
    "click",
    function (event) {

        // VERY IMPORTANT:
        // Prevent form/page refresh.

        event.preventDefault();


        console.log(
            "Talk button clicked."
        );


        // Prevent double clicking.

        if (isListening) {

            console.log(
                "Already listening."
            );

            return;

        }


        if (!recognition) {

            console.error(
                "Recognition is not available."
            );

            return;

        }


        try {

            recognition.start();

        }

        catch (error) {

            console.error(
                "Could not start recognition:",
                error
            );

        }

    }
);
