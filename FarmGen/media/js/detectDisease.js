document.getElementById("probableImageRow").hidden = true
document.getElementById("final_disease").hidden = true

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
                            count += 1
                        }
                      }
                    document.getElementById("probableImageRow").hidden = false
                } else {
                    document.getElementById("probableImageRow").hidden = true
                    document.getElementById("final_disease").textContent = `Detected Disease is: ${result.result_disease}`
                    document.getElementById("final_disease").hidden = false
                }
            } else {
                alert("Image upload failed.");
            }
        } catch (error) {
            console.error('Error uploading image:', error);
        }
    }
}