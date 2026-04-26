document.getElementById("askBtn").addEventListener("click", async () => {

    const question = document.getElementById("question").value;
    const answerBox = document.getElementById("answer");

    answerBox.innerText = "Thinking...";

    chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {

        const payload = {
            url: tabs[0].url,
            question: question
        };

        console.log("📦 Sending:", payload);

        try {
            const res = await fetch("http://127.0.0.1:8000/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const data = await res.json();

            console.log("🧠 Response:", data);

            answerBox.innerText = data.answer;

        } catch (err) {
            console.log(err);
            answerBox.innerText = "Backend error";
        }
    });
});