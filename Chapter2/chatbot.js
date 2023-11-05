document.addEventListener("DOMContentLoaded", function () {
    const startButton = document.getElementById("startButton");
    const clearButton = document.getElementById("clearButton");
    const status = document.getElementById("status");
    const outputArea = document.getElementById("outputArea");
    const template =
        "あなたは音声対話型チャットボットです。なるべく短い文章で回答してください。";
    const messages = [
        {
            role: "system",
            content: template,
        },
    ];
    let recognition;

    startButton.addEventListener("click", () => {
        console.log("startButton clicked");
        const apiKey = document.getElementById("apiKey").value;
        if (!recognition) {
            recognition = new webkitSpeechRecognition();
            recognition.onstart = function () {
                status.innerHTML = "音声認識中";
            };
            recognition.onend = function () {
                status.innerHTML = "音声認識終了";
            };
            recognition.onresult = async function (event) {
                const result = event.results[0][0].transcript;
                messages.push({
                    role: "user",
                    content: result,
                });
                console.log(messages);
                outputArea.innerHTML =
                    outputArea.innerHTML + "あなた： " + result + "<br/>";
                status.innerHTML = "考え中・・・";
                const response = await fetch(
                    "https://api.openai.com/v1/chat/completions",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${apiKey}`,
                        },
                        body: JSON.stringify({
                            model: "gpt-3.5-turbo",
                            messages: messages,
                        }),
                    }
                );
                const responseJson = await response.json();
                const botMessage = responseJson.choices[0].message.content;
                messages.push({
                    role: "assistant",
                    content: botMessage,
                });
                console.log(messages);
                outputArea.innerHTML =
                    outputArea.innerHTML + "ボット： " + botMessage + "<br/>";
                speak(botMessage);
                status.innerHTML = "開始ボタンをクリックして話しかけてください。";
            };
        }
        recognition.start();
    });

    clearButton.addEventListener("click", () => {
        console.log("clearButton clicked");
        if (recognition) {
            recognition.stop();
            recognition = null;
        }
        messages.length = 0;
        messages.push({
            role: "system",
            content: template,
        });
        console.log(messages);
        outputArea.innerHTML = "";
    });

    function speak(text) {
        const utterance = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(utterance);
    }
});
