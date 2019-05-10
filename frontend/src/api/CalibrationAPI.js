const axios = require('axios');
const BASE_URL = "http://localhost:5050";

export const getCalibrationFactors = async (model, isotope) => {
    let endpoint = BASE_URL + "/calibrations";
    return await axios.get(endpoint, {
        params: {
            model: model,
            isotope: isotope
        }})
};

export const getCounters = async () => {
    let endpoint = BASE_URL + "/counters";
    return await axios.get(endpoint);
};

export const getIsotopes = async () => {
    let endpoint = BASE_URL + "/isotopes";
    return await axios.get(endpoint);
}