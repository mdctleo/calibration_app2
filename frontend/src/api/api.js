const axios = require('axios');
const BASE_URL = " http://localhost:5000";


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
export const postBiodiCsv = async (payload) => {
    let endpoint = BASE_URL + "/biodicsv"
    let data = new FormData()
    console.log(payload.biodiCsvs)
    console.log(payload.mouseCsvs)
    console.log(payload.organCsvs)

    data.append("studyInfo", new Blob([JSON.stringify(payload.studyInfo)], {type: 'application/json'}))
    // data.append("gammaInfo", new Blob([JSON.stringify(payload.gammaInfo)], {type: 'application/json'}))

    for (let i = 0; i < payload.biodiCsvs.length; i++) {
        data.append("gammaInfo" + i, new Blob([JSON.stringify(
            {gammaCounter: payload.gammaInfo.gammaCounter[i],
             gammaCounterRunTimeOffset: payload.gammaInfo.gammaCounterRunTimeOffset[i] === undefined ? '' : payload.gammaInfo.gammaCounterRunTimeOffset[i],
             gammaCounterRunComments: payload.gammaInfo.gammaCounterRunComments[i] === undefined ? '' : payload.gammaInfo.gammaCounterRunComments[i]
        })], {type: 'application/json'}))
        data.append("biodiCsvs" + i, new Blob([payload.biodiCsvs[i]], {type: payload.biodiCsvs[i].type}))
        data.append("mouseCsvs" + i, new Blob([payload.mouseCsvs[i]],  {type: payload.mouseCsvs[i].type}))
        data.append("organCsvs" + i, new Blob([payload.organCsvs[i]], {type: payload.organCsvs[i].type}))
    }
    console.log(data)
    return await axios({
        method: 'post',
        url: endpoint,
        data: data,
        config: { headers: {'Content-Type': 'multipart/form-data'}}
    })
};

export const getBiodiCsvMetas = async () => {
    let endpoint = BASE_URL + "/biodicsv-metas";
    return await axios.get(endpoint);
};

export const getBiodiCsvComplete = async (id) => {
    let endpoint = BASE_URL + "/biodicsv-complete";
    return await axios.get(endpoint, {
        responseType: 'blob',
        params: {
            id: id
        }
    })
};

export const getBiodiCsv = async (id) => {
    let endpoint = BASE_URL + "/biodicsv"
    return await axios.get(endpoint, {
        responseType: 'blob',
        params: {
            id: id
        }
    })
}

export const getBiodiCsvAnalysis = async (id) => {
    let endpoint = BASE_URL + "/biodicsv-analysis"
    return await axios.get(endpoint, {
        responseType: 'blob',
        params: {
            id: id
        }
    })
}

export const getChelators = async () => {
    let endpoint = BASE_URL + "/chelators"
    return await axios.get(endpoint)
}

export const getVectors = async () => {
    let endpoint = BASE_URL + "/vectors"
    return await axios.get(endpoint)
}

export const getMouseStrains = async () => {
    let endpoint = BASE_URL + "/mouse-strains"
    return await axios.get(endpoint)
}

export const getTumorModels = async () => {
    let endpoint = BASE_URL + "/tumor-models"
    return await axios.get(endpoint)
}

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

// User
export const login = async (loginForm) => {
    let endpoint = BASE_URL + "/login"
    return await axios.post(endpoint, {
        email: loginForm.email,
        password: loginForm.password
    })
}

export const logout = async () => {
    let endpoint = BASE_URL + "/logout"
    return await axios.delete(endpoint)
}