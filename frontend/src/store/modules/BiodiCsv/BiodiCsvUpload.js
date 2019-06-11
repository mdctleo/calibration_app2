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
    setUploadFile: (context, payload) => {
        context.commit('SET_UPLOAD_FILE', payload);
    },

    setStudyName: (context, payload) => {
        context.commit('SET_STUDY_NAME', payload);
    },

    setStudyDate: (context, payload) => {
        context.commit('SET_STUDY_DATE', payload)
    },

    setResearcherName: (context, payload) => {
        context.commit('SET_RESEARCHER_NAME', payload)
    },

    setPiName: (context, payload) => {
        context.commit('SET_PI_NAME', payload)
    },

    setRadioIsotope: (context, payload) => {
        context.commit('SET_RADIO_ISOTOPE', payload)
    },

    setRadioTracer: (context, payload) => {
        context.commit('SET_RADIO_TRACER', payload)
    },

    setComments: (context, payload) => {
        context.commit('SET_COMMENTS', payload)
    },

    setGammaCounters: (context, payload) => {
        context.commit('SET_GAMMA_COUNTERS', payload)
    },

    setMice: (context, payload) => {
        context.commit('SET_MICE', payload)
    },

    setOrgans: (context, payload) => {
        context.commit('SET_ORGANS', payload)
    },

    setError: (context, payload) => {
        context.commit('SET_ERROR', payload)
    },

    /**
     * File upload start
    **/
    handleRawFile: (context, payload) => {
        context.commit('SET_LOADING', {loading: true});
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
                context.commit('SET_ERROR', {error: error.response.data.message})
            })
            .finally(() => {
                context.commit('SET_LOADING', {loading: false});
                context.commit('SET_UPLOAD_FILE', {file: null})

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

const mutations = {
    SET_LOADING: (state, payload) => {
        return state.loading = payload.loading;
    },

    SET_ERROR: (state, payload) => {
        return state.error = payload.error;
    },

    SET_UPLOAD_FILE: (state, payload) => {
        return state.file = payload.file
    },

    SET_STUDY_NAME: (state, payload) => {
        return state.studyName = payload.studyName
    },

    SET_STUDY_DATE: (state, payload) => {
        return state.studyDate = payload.studyDate
    },

    SET_RESEARCHER_NAME: (state, payload) => {
        return state.researcherName = payload.researcherName
    },

    SET_PI_NAME: (state, payload) => {
        return state.piName = payload.piName
    },

    SET_RADIO_ISOTOPE: (state, payload) => {
        return state.radioIsotope = payload.radioIsotope
    },

    SET_RADIO_TRACER: (state, payload) => {
        return state.radioTracer = payload.radioTracer
    },

    SET_COMMENTS: (state, payload) => {
        return state.comments = payload.comments
    },

    SET_GAMMA_COUNTERS: (state, payload) => {
        return state.gammaCounters = payload.gammaCounters
    },

    SET_MICE: (state, payload) => {
        return state.mice = payload.mice
    },

    SET_ORGANS: (state, payload) => {
        return state.organs = payload.organs
    },

};

const getters = {
    studyName: state => state.studyName,
    studyDate: state => state.studyDate,
    researcherName: state => state.researcherName,
    piName: state => state.piName,
    radioIsotope: state => state.radioIsotope,
    radioTracer: state => state.radioTracer,
    comments: state => state.comments,
    gammaCounters: state => state.gammaCounters,
    mice: state => state.mice,
    organs: state => state.organs,
    file: state => state.file,
    loading: state => state.loading,
    error: state => state.error
};

export default {
    state: defaultState,
    getters,
    actions,
    mutations,
    namespaced: true
};