document.getElementById("probableImageRow").hidden = true
document.getElementById("final_disease").hidden = true
document.getElementById("cure_details_div").hidden = true

async function uploadImage() {
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput.files[0];
    
    if (file) {
        const formData = new FormData();
        formData.append('diseaseFile', file);

        try {
            const response = await fetch('/uploadimagedisease/', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                // Handle the JSON response from the server
                var count = 1
                if(result.type == "ProbableImages"){
                    document.getElementById("final_disease").hidden = true
                    for (const [key, value] of Object.entries(result.suggested_images)) {
                        for (let index = 0; index < value.length; index++) {
                            document.getElementById(`probabledisease${count}`).src = `/media/images/DiseaseDetectionImageDataset/${key}/${value[index]}`

                            document.getElementById(`buttonprobabledisease${count}`).addEventListener('click',displayDetectedDisease.bind(this, key))
                            count += 1
                        }
                      }
                    document.getElementById("probableImageRow").hidden = false
                } else {
                    await displayDetectedDisease(result.result_disease)
                }
            } else {
                alert("Image upload failed.");
            }
        } catch (error) {
            console.error('Error uploading image:', error);
        }
    }
}

async function displayDetectedDisease(disease_name){
    console.log("Here")
    document.getElementById("probableImageRow").hidden = true
    document.getElementById("final_disease").textContent = `Detected Disease is: ${disease_name}`
    document.getElementById("final_disease").hidden = false
    await getBedrockResponse(disease_name)
}

async function getBedrockResponse(disease_name) {
    const formData = new FormData();
    formData.append('disease_name', disease_name);

    try {
        const response = await fetch('/getbedrockresponse/', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const result = await response.json();
            // Handle the JSON response from the server
            if(result.status == "Success"){
                document.getElementById("cure_details_div").hidden = false
                document.getElementById("detail_p").innerHTML = result.response
                document.getElementById("detail_audio").src = "/media/audiofiles/" + result.audio_filename
            } else {
                console.log("Error: " + result.response)
            }
        } else {
            alert("Failed to get Response!");
        }
    } catch (error) {
        console.error('Error Calling bedrock:', error);
    }
}