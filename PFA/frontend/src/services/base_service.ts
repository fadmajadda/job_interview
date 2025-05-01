import axios from "axios";


const Api = () => {
    return axios.create({
        baseURL: 'http://localhost:5000',
        timeout: 180000,
        withCredentials: false, // Disable credentials
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    });
}

export default Api;