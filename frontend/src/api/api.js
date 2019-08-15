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
export const postBiodiCsvTest = async (payload) => {
    let endpoint = BASE_URL + "/biodicsv-test"
    let data = new FormData()
    let mouseInfo = JSON.stringify(payload.mouseInfo)
    console.log(mouseInfo)
    data.append("studyInfo", new Blob([JSON.stringify(payload.studyInfo)], {type: 'application/json'}))
    data.append("gammaInfo", new Blob([JSON.stringify(payload.gammaInfo)], {type: 'application/json'}))
    data.append("biodiFile", new Blob([payload.biodiCsv], {type: payload.biodiCsv.type}))
    data.append("mouseInfo", new Blob([JSON.stringify(payload.mouseInfo)], {type: 'application/json'}))
    data.append("organInfo", new Blob([JSON.stringify(payload.organInfo)], {type: 'application/json'}))
    return await axios({
        method: 'post',
        url: endpoint,
        data: data,
        config: { headers: {'Content-Type': 'multipart/form-data'}}
    })

}

export const postBiodiCsv = async (payload) => {
    let endpoint = BASE_URL + "/biodicsv";
    return await axios.post(endpoint, {
        biodiCsv: payload.biodiCsv,
        studyInfo: payload.studyInfo,
        gammaInfo: payload.gammaInfo,
        mouseInfo: payload.mouseInfo,
        organInfo: payload.organInfo
    })
};

export const getBiodiCsvMetas = async () => {
    let endpoint = BASE_URL + "/biodicsv-metas";
    return await axios.get(endpoint);
};

export const getBiodiCsvComplete = async (id) => {
    let endpoint = BASE_URL + "/biodicsv";
    return await axios.get(endpoint, {
        responseType: 'blob',
        params: {
            id: id
        }
    })
};

export const getBiodiCsvRaw = async (id) => {
    let endpoint = BASE_URL + "/biodicsv-raw"
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

export const getCellLines = async () => {
    let endpoint = BASE_URL + "/cell-lines"
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