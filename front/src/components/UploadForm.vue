<template>
    <form action="">
        <div class="mb-3">
            <label for="formFile" class="form-label">Upload your image</label>
            <input class="form-control" type="file" accept="image/*" id="formFile" @change="uploadImage">
        </div>
    </form>

    <div class="row">
        <div class="col-12">
            <div ref="preview"></div>
        </div>
    </div>

    <div class="crop__container" :class="{ 'd-none': !isUploaded }">
        <div class="container">
            <div class="row d-flex justify-content-center">
                <div class="col-5 mt-5">
                    <div ref="crop"></div>
                    <div class="d-flex justify-content-center">
                        <button class="btn btn-primary btn-block mt-3" @click="cropImage">Crop</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import Croppie from 'croppie';

import { generateImage } from '../services/upload.service';

import 'croppie/croppie.css';


const crop = ref(null);
const preview = ref(null);
const cropData = ref(null);
const isUploaded = ref(false);

onMounted(() => {
    const data = new Croppie(crop.value, {
        viewport: { width: 200, height: 200 },
        boundary: { width: 300, height: 300 },
        showZoomer: true,
        enableOrientation: true,
        enableExif: true,
        enableZoom: true,
        enableZoomer: true,
    });

    cropData.value = data;
});

const cropImage = () => {
    cropData.value.result('base64').then((res) => {

        const image = new Image();
        image.src = res;
        image.classList.add('img-fluid', 'mr-2');

        generateImage(res).then((result) => {
            console.log(result);
            
            isUploaded.value = false;
            preview.value.appendChild(image);

        }).catch((err) => {
            console.log(err);
        });





    });
}

const uploadImage = (e) => {

    const reader = new FileReader();
    reader.readAsDataURL(e.target.files[0]);

    reader.onload = (e) => {
        isUploaded.value = true;

        cropData.value.bind({
            url: e.target.result,
        });


    }
}


</script>

<style scoped>
.crop__container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.3);
}
</style>