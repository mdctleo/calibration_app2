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
}

export const getCalibrationFactorsGraph = async (model, isotope) => {
    let endpoint = BASE_URL + "/calibrations/graph";
    return await axios.get(endpoint, {
        params: {
            model: model,
            isotope: isotope
        }})
};

export const postCsvFiles = async (files) => {
    let endpoint = BASE_URL + "/csv";
    let data = new FormData();
    data.append('file', files[0]);
    console.log(data);
    return await axios({
        method: 'post',
        url: endpoint,
        data: data,
        charset: "ISO-8859-1",
        config: { headers: {'Content-Type': 'multipart/form-data'}}
    })
};