import axios from "axios";


const Api = () => {
    return axios.create({
        baseURL: import.meta.env.VITE_API_BASE_URL,
        timeout: 180000,
        withCredentials: false, // Disable credentials
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    });
}

export default Api;