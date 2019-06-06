const axios = require('axios');
const BASE_URL = " http://15305a13.ngrok.io";


// Calibration

export const getCalibrationFactors = async (model, isotope) => {
    let endpoint = BASE_URL + "/calibrations";
    return await axios.get(endpoint, {
        params: {
            model: model,
            isotope: isotope
        }
    })
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
        }
    })
};

// BiodiCsv

export const postBiodiCsvFiles = async (filesJson) => {
    let endpoint = BASE_URL + "/biodicsv";
    return await axios.post(endpoint, {
        files: filesJson
    })
};

export const getBiodiCsvMetas = async () => {
    let endpoint = BASE_URL + "/biodicsv-metas";
    return await axios.get(endpoint);
};

export const getBiodiCsv = async (id) => {
    let endpoint = BASE_URL + "/biodicsv";
    return await axios.get(endpoint, {
        responseType: 'blob',
        params: {
            id: id
        }
    })
};

// Statistics

export const calculateEffect = async (statisticForm) => {
    let endpoint = BASE_URL + "/effectCalc";
    return await axios.get(endpoint, {
        params: {
            nobs: statisticForm.nobs,
            power: statisticForm.power,
            alpha: statisticForm.alpha,
            test: statisticForm.test,
            alternative: statisticForm.alternative
        }
    })
};

export const calculateNobs = async (statisticForm) => {
    let endpoint = BASE_URL + "/nobsCalc";
    return await axios.get(endpoint, {
        params: {
            effect: statisticForm.effect,
            power: statisticForm.power,
            alpha: statisticForm.alpha,
            test: statisticForm.test,
            alternative: statisticForm.alternative
        }
    })
};

export const calculatePower = async (statisticForm) => {
    let endpoint = BASE_URL + "/powerCalc";
    return await axios.get(endpoint, {
        params: {
            effect: statisticForm.effect,
            nobs: statisticForm.nobs,
            alpha: statisticForm.alpha,
            test: statisticForm.test,
            alternative: statisticForm.alternative
        }
    })
};

export const getPowerGraph = async (statisticForm) => {
    let endpoint = BASE_URL + "/powerCalcGraph";
    return await axios.get(endpoint, {
        params: {
            effect: statisticForm.effect,
            nobs: statisticForm.nobs,
            alpha: statisticForm.alpha,
            test: statisticForm.test,
            alternative: statisticForm.alternative
        }
    })
};

export const getPowerTable = async (statisticForm) => {
    let endpoint = BASE_URL + "/powerCalcTable";
    return await axios.get(endpoint, {
        params: {
            effect: statisticForm.effect,
            nobs: statisticForm.nobs,
            alpha: statisticForm.alpha,
            test: statisticForm.test,
            alternative: statisticForm.alternative
        }
    })
};