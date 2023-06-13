import axios from 'axios';

const API_URL = 'http://localhost:8000/upload-image/';

const api = axios.create({
    baseURL: API_URL,
});


export const generateImage = async (file) => {

    return await api.post('', {
        file: file,
    }, {
        headers: {
            'Accept': 'application/json',
        },
    });
}