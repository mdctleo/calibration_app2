import * as api from '../../api/CalibrationAPI'


export const getCalibrationFactors = (model, isotope) => {
    console.log("initiate call");
    api.getCalibrationFactors(model, isotope)
        .then((response) => {
            return response.data;
        })
        .catch((error) => {
            console.log(error)

        })
};

export const getCounters = () => {
    console.log("initiate call");
    api.getCounters()
        .then((response) => {
           return response.data;
        })
        .catch((error) => {
            console.log(error)

        })
};

export const getIsotopes = () => {
    console.log("initiate call");
    api.getIsotopes()
        .then((response) => {
           return response.data;
        })
        .catch((error) => {
            console.log(error)

        })
};
