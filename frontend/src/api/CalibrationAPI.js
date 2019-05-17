const axios = require('axios');
const BASE_URL = " http://localhost:5000";

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
};

export const getCalibrationFactorsGraph = async (model, isotope) => {
    let endpoint = BASE_URL + "/calibrations/graph";
    return await axios.get(endpoint, {
        params: {
            model: model,
            isotope: isotope
        }})
};

export const postCsvFiles = async (filesJson) => {
    let endpoint = BASE_URL + "/csv";
    return await axios.post(endpoint, {
        files: filesJson
    })
};