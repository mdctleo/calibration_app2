import {postBiodiCsvFile} from "../../../api/api";

const moment = require('moment');
const csv = require('csvtojson');

const defaultState = {
    studyName: "",
    studyDate: "",
    researcherName: "",
    piName: "",
    radioIsotope: "",
    radioTracer: "",
    comments: "",
    gammaCounters: [],
    mice: [],
    organs: [],
    file: null,
    loading: false,
    error: null
};

const actions = {
    setBiodiCSvUploadFile: (context, payload) => {
      context.commit('SET_BIODI_CSV_UPLOAD_FILE', payload);
    },

    setStudyName: (context, payload) => {

    },


    /**
     * File upload start
    **/
    handleRawFile: (context, payload) => {
        context.commit('SET_BIODI_CSV_UPLOAD_LOADING', {loading: true});
        this.readFile(payload.file)
            .then((csvFile) => {
                return csv().fromString(csvFile)
            })
            .then((csvFileJson) => {
                let fileFormat = {
                    fileName: payload.file.name,
                    file: csvFileJson
                };

                return postBiodiCsvFile(fileFormat)
            })
            .then((rsponse) => {

            })
            .catch((error) => {
                context.commit('SET_BIODI_CSV_UPLOAD_ERROR', {error: error.response.data.message})
            })
            .finally(() => {
                context.commit('SET_BIODI_CSV_UPLOAD_LOADING', {loading: false});
                context.commit('SET_BIODI_CSV_UPLOAD_FILE', {file: null})

            })
    },

    readFile(file) {
        return new Promise((resolve, reject) => {
            let fileReader = new FileReader();

            fileReader.onerror = () => {
                fileReader.abort();
                reject("Something went wrong");
            };

            fileReader.onload = () => {
                resolve(fileReader.result);
            };

            fileReader.readAsText(file)
        })
    },

    replaceProtocolKey(csvRow) {
        let protocolName = csvRow['Protocol name'];
        let oldCountKey = protocolName + ' Counts';
        let oldCPMKey = protocolName + ' CPM';
        let oldErrorKey = protocolName + ' Error %';
        let oldInfoKey = protocolName + ' Info';

        csvRow['Counts'] = csvRow[oldCountKey];
        csvRow['CPM'] = csvRow[oldCPMKey];
        csvRow['Error %'] = csvRow[oldErrorKey];
        csvRow['Info'] = csvRow[oldInfoKey];

        delete csvRow[oldCountKey];
        delete csvRow[oldCPMKey];
        delete csvRow[oldErrorKey];
        delete csvRow[oldInfoKey];
        delete csvRow['Protocol name'];
    }
    /**
     * File upload ends
     */
};

// studyName: "",
//     studyDate: "",
//     researcherName: "",
//     piName: "",
//     radioIsotope: "",
//     radioTracer: "",
//     comments: "",
//     gammaCounters: [],
//     mice: [],
//     organs: [],
//     file: null,
//     loading: false,
//     error: null

const mutations = {
    SET_BIODI_CSV_UPLOAD_LOADING: (state, payload) => {
        return state.loading = payload.loading;
    },

    SET_BIODI_CSV_UPLOAD_ERROR: (state, payload) => {
        return state.error = payload.error;
    },

    SET_BIODI_CSV_UPLOAD_FILE: (state, payload) => {
        return state.file = payload.file
    }
};

const getters = {

};

export default {
    state: defaultState,
    getters,
    actions,
    mutations,
};