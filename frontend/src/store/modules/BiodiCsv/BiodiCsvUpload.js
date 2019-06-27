import {postBiodiCsv} from "../../../api/api";

const moment = require('moment');
const csv = require('csvtojson');

const defaultState = {
    studyForm: {
        studyName: "",
        studyDate: "",
        researcherName: "",
        piName: "",
        radioIsotope: "",
        chelator: "",
        vector: "",
        target: "",
        cellLine: "",
        mouseStrain: "",
        tumorModel: "",
        radioActivity: "",
        radioPurity: "",
        comments: "",
    },

    gammaForm: {
        gammaCounter: "",
        gammaCounterRunDateTime: "",
        gammaCounterRunTimeOffset: "",
        gammaCounterRunComments: "",
    },

    organForm: {
        selectedOrgans: []
    },

    mice: [],
    availableOrgans: ["Lungs", "Liver", "Heart"],
    biodiCsvs: null,
    biodiCsvJson: null,
    loading: false,
    error: null,
    startValidation: false,
    mouseCsvFormat: "Mouse ID, Gender, Age, Group ID, Euthanasia Date, Euthanasia Time, Weight (g), Injection Date, Pre-Injection Time, Injection Time, Post-Injection Time, Pre-Injection MBq, Post-Injection MBq, Comments",
    mouseCsv: null,
    mouseCsvJson: null,
    organCsvFormat: "Organ Order",
    organCsv: null,
};

const actions = {
    setStartValidation: (context, payload) => {
        context.commit('SET_START_VALIDATION', payload)
    },

    setStudyName: (context, payload) => {
        context.commit('SET_STUDY_NAME', payload)
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

    setChelator: (context, payload) => {
        context.commit('SET_CHELATOR', payload)
    },

    setVector: (context, payload) => {
        context.commit('SET_VECTOR', payload)
    },

    setTarget: (context, payload) => {
        context.commit('SET_TARGET', payload)
    },

    setCellLine: (context, payload) => {
        context.commit('SET_CELL_LINE', payload)
    },

    setMouseStrain: (context, payload) => {
        context.commit('SET_MOUSE_STRAIN', payload)
    },

    setTumorModel: (context, payload) => {
        context.commit('SET_TUMOR_MODEL', payload)
    },

    setRadioActivity: (context, payload) => {
        context.commit('SET_RADIO_ACTIVITY', payload)
    },

    setRadioPurity: (context, payload) => {
        context.commit('SET_RADIO_PURITY', payload)
    },

    setComments: (context, payload) => {
        context.commit('SET_COMMENTS', payload)
    },

    setGammaCounter: (context, payload) => {
        context.commit('SET_GAMMA_COUNTER', payload)
    },

    setGammaCounterRunDateTime: (context, payload) => {
        context.commit('SET_GAMMA_COUNTER_RUN_DATE_TIME', payload)
    },

    setGammaCounterRunTimeOffset: (context, payload) => {
        context.commit('SET_GAMMA_COUNTER_RUN_TIME_OFFSET', payload)
    },

    setGammaCounterRunComments: (context, payload) => {
        context.commit('SET_GAMMA_COUNTER_RUN_COMMENTS', payload)
    },

    setMice: (context, payload) => {
        context.commit('SET_MICE', payload)
    },

    setMouseCsv: (context, payload) => {
        context.commit('SET_MOUSE_CSV', payload)
    },

    setOrganCsv: (context, payload) => {
        context.commit('SET_ORGAN_CSV', payload)
    },

    setSelectedOrgan: (context, payload) => {
        context.commit('SET_SELECTED_ORGAN', payload)
    },

    setBiodiCsvs: (context, payload) => {
        context.commit('SET_BIODI_CSVS', payload)
    },

    setError: (context, payload) => {
        context.commit('SET_ERROR', payload)
    },

    downloadMouseCsvFormat: (context) => {
        const url = window.URL.createObjectURL(new Blob([context.state.mouseCsvFormat]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'mouse_info.csv');
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);
    },

    downloadOrganCsvFormat: (context) => {
        const url = window.URL.createObjectURL(new Blob([context.state.organCsvFormat]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'organ_order.csv');
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);
    },

    readFile: (context, file) => {
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

    validateMouse: (context, row) => {
        if (row['Mouse ID'] === "") {
            return false
        } else if (row['Gender'] === "") {
            return false
        } else if (row['Age'] === "") {
            return false
        } else if (row['Group ID'] === "") {
            return false
        } else if (row['Euthanasia Date'] === "" || !moment(row['Euthanasia Date'], "YYYY-MM-DD", true).isValid()) {
            return false
        } else if (row['Euthanasia Time'] === "" || !moment(row['Euthanasia Time'], "HH:mm", true).isValid()) {
            return false
        } else if (row['Weight (g)'] === "") {
            return false
        } else if (row['Injection Date'] === "" || !moment(row['Injection Date'], "YYYY-MM-DD", true).isValid()) {
            return false
        } else if (row['Pre-Injection Time'] === "" || !moment(row['Pre-Injection Time'], "HH:mm", true).isValid()) {
            return false
        } else if (row['Injection Time'] === "" || !moment(row['Injection Time'], "HH:mm", true).isValid()) {
            return false
        } else if (row['Post-Injection Time'] === "" || !moment(row['Post-Injection Time'], "HH:mm", true).isValid()) {
            return false
        } else if (row['Pre-Injection MBq'] === "") {
            return false
        } else if (row['Post-Injection MBq'] === "") {
            return false
        } else {
            return true;
        }
    },


    handleMouseCsv: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true})
            // did not upload file
            if (payload.mouseCsv === null) {
                context.commit('SET_ERROR', {error: "mouse csv not uploaded"})
                return false
            }
            let mouseCsv = payload.mouseCsv[0].raw

            let csvFile = await context.dispatch('readFile', mouseCsv)
            // validate headers
            if (csvFile.substring(0, context.state.mouseCsvFormat.length) !== context.state.mouseCsvFormat) {
                context.commit('SET_ERROR', {error: "Do not mess with the headers"})
                return false
            }
            let csvFileJson = await csv().fromString(csvFile)
            let indexHolder = 0
            let rowValidated = true

            // validate each existing rows for required cells
            for (let i = 0; i < csvFileJson.length; i++) {
                let row = csvFileJson[i]
                indexHolder = i
                rowValidated = await context.dispatch('validateMouse', row)

                if (!rowValidated) {
                    break
                }
            }

            if (rowValidated) {
                context.commit('SET_MOUSE_CSV_JSON', {mouseCsvJson: csvFileJson})
                return true
            } else {
                context.commit('SET_ERROR', {error: "There is an error on row " + (indexHolder + 2)})
                return false
            }
        } catch (err) {
            context.commit('SET_ERROR', {error: err.message})
            return false
        } finally {
            context.commit('SET_LOADING', {loading: false})
        }
    },

    handleOrganCsv: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true});
            if (payload.organCsv === null) {
                context.commit('SET_ERROR', {error: "organ csv not uploaded"});
                return context.commit('SET_SELECTED_ORGANS', {selectedOrgans: []})
            }

            let organCsv = payload.organCsv[0].raw;

            let csvFile = await context.dispatch('readFile', organCsv);
            // validate headers
            if (csvFile.substring(0, context.state.organCsvFormat.length) !== context.state.organCsvFormat) {
                context.commit('SET_ERROR', {error: "Do not mess with the headers"});
                return false;
            }

            let csvFileJson = await csv().fromString(csvFile);

            let selectedOrgans = [];
            for (let i = 0; i < csvFileJson.length; i++) {
                selectedOrgans.push({
                    key: i,
                    label: i,
                    type: 'OrganForm',
                    value: csvFileJson[i]['Organ Order']
                })
            }

            return context.commit('SET_SELECTED_ORGANS', {selectedOrgans: selectedOrgans})
        } catch (err) {
            context.commit('SET_ERROR', {error: err.message});
            return false;
        } finally {
            context.commit('SET_LOADING', {loading: false});
        }
    },

    validateBiodiCsvs: (context, row) => {
        if (row['Protocol ID'] === "") {
            return false
        } else if (row['Measurement date & time'] === "" || !moment(row['Measurement date & time'], "YYYY-MM-DD HH:mm", true).isValid()) {
            console.log("measurement date & time validation failed")
            return false
        } else if (row['Completion status'] === "") {
            return false
        } else if (row['Run ID'] === "") {
            return false
        } else if (row['Rack'] === "") {
            return false
        } else if (row['Det'] === "") {
            return false
        } else if (row['Pos'] === "") {
            return false
        } else if (row['Time'] === "") {
            return false
        } else if (row['Counts'] === "") {
            return false
        } else if (row['CPM'] === "") {
            return false
        } else if (row['Error %'] === "") {
            return false
        } else {
            return true
        }
    },

    /**
     * File upload start
     **/
    handleBiodiCsvs: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true});
            if (payload.biodiCsvs === null) {
                context.commit('SET_ERROR', {error: "biodi csv not uploaded"})
                return false
            }
            let biodiCsvFile = payload.biodiCsvs[0]
            let csvFile = await context.dispatch('readFile', biodiCsvFile.raw)
            let csvFileJson = await csv().fromString(csvFile)
            let rowValidated = true
            let indexHolder = 0


            for (let i = 0; i < csvFileJson.length; i++) {
                indexHolder = i
                let csvRow = csvFileJson[i]
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

                rowValidated = await context.dispatch('validateBiodiCsvs', csvRow)
                if (!rowValidated) {
                    break
                }
            }

            if (rowValidated) {
                let fileFormat = {
                    fileName: biodiCsvFile.name,
                    file: csvFileJson
                };

                context.commit('SET_BIODI_CSV_JSON', {biodiCsvJson: fileFormat})
                return true
            } else {
                context.commit('SET_ERROR', {error: "There is an error on row " + (indexHolder + 2)})
                return false

            }

        } catch (error) {
            context.commit('SET_ERROR', {error: error.response.data.message})
            return false
        } finally {
            context.commit('SET_LOADING', {loading: false});
        }
    },


    /**
     * File upload ends
     */
    postBiodiCsv(context, payload) {
        console.log(payload)
        context.commit('SET_LOADING', {loading: true})
        postBiodiCsv(payload)
            .then((response) => {
                console.log(response)
            })
            .catch((error) => {
                context.commit('SET_ERROR', {error: error.response.data.message})
            })
            .finally(() => {
                context.commit('SET_LOADING', {loading: false})
            })
    }


};

const mutations = {
    SET_START_VALIDATION: (state, payload) => {
        return state.startValidation = payload.startValidation
    },

    SET_LOADING: (state, payload) => {
        return state.loading = payload.loading;
    },

    SET_ERROR: (state, payload) => {
        return state.error = payload.error;
    },

    SET_STUDY_NAME: (state, payload) => {
        return state.studyForm.studyName = payload.studyName
    },

    SET_STUDY_DATE: (state, payload) => {
        return state.studyForm.studyDate = payload.studyDate
    },

    SET_RESEARCHER_NAME: (state, payload) => {
        return state.studyForm.researcherName = payload.researcherName
    },

    SET_PI_NAME: (state, payload) => {
        return state.studyForm.piName = payload.piName
    },

    SET_RADIO_ISOTOPE: (state, payload) => {
        return state.studyForm.radioIsotope = payload.radioIsotope
    },

    SET_CHELATOR: (state, payload) => {
        return state.studyForm.chelator = payload.chelator
    },

    SET_VECTOR: (state, payload) => {
        return state.studyForm.vector = payload.vector
    },

    SET_TARGET: (state, payload) => {
        return state.studyForm.target = payload.target
    },

    SET_CELL_LINE: (state, payload) => {
        return state.studyForm.cellLine = payload.cellLine
    },

    SET_MOUSE_STRAIN: (state, payload) => {
        return state.studyForm.mouseStrain = payload.mouseStrain
    },

    SET_TUMOR_MODEL: (state, payload) => {
        return state.studyForm.tumorModel = payload.tumorModel
    },

    SET_RADIO_ACTIVITY: (state, payload) => {
        return state.studyForm.radioActivity = payload.radioActivity
    },

    SET_RADIO_PURITY: (state, payload) => {
        return state.studyForm.radioPurity = payload.radioPurity
    },

    SET_COMMENTS: (state, payload) => {
        return state.studyForm.comments = payload.comments
    },

    SET_GAMMA_COUNTER: (state, payload) => {
        return state.gammaForm.gammaCounter = payload.gammaCounter
    },

    SET_GAMMA_COUNTER_RUN_DATE_TIME: (state, payload) => {
        return state.gammaForm.gammaCounterRunDateTime = payload.gammaCounterRunDateTime
    },

    SET_GAMMA_COUNTER_RUN_TIME_OFFSET: (state, payload) => {
        return state.gammaForm.gammaCounterRunTimeOffset = payload.gammaCounterRunTimeOffset
    },

    SET_GAMMA_COUNTER_RUN_COMMENTS: (state, payload) => {
        return state.gammaForm.gammaCounterRunComments = payload.gammaCounterRunComments
    },

    SET_MICE: (state, payload) => {
        return state.mice = payload.mice
    },

    SET_AVAILABLE_ORGANS: (state, payload) => {
        return state.availableOrgans = payload.availableOrgans
    },

    SET_SELECTED_ORGANS: (state, payload) => {
        return state.organForm.selectedOrgans = payload.selectedOrgans
    },

    SET_SELECTED_ORGAN: (state, payload) => {
        return state.organForm.selectedOrgans[payload.index].value = payload.organ
    },

    SET_MOUSE_CSV: (state, payload) => {
        return state.mouseCsv = payload.mouseCsv
    },

    SET_MOUSE_CSV_JSON: (state, payload) => {
        return state.mouseCsvJson = payload.mouseCsvJson
    },

    SET_ORGAN_CSV: (state, payload) => {
        return state.organCsv = payload.organCsv
    },

    SET_BIODI_CSVS: (state, payload) => {
        return state.biodiCsvs = payload.biodiCsvs
    },

    SET_BIODI_CSV_JSON: (state, payload) => {
        return state.biodiCsvJson = payload.biodiCsvJson
    }
};

const getters = {
    startValidation: state => state.startValidation,

    studyForm: state => state.studyForm,
    studyName: state => state.studyForm.studyName,
    studyDate: state => state.studyForm.studyDate,
    researcherName: state => state.studyForm.researcherName,
    piName: state => state.studyForm.piName,
    radioIsotope: state => state.studyForm.radioIsotope,
    chelator: state => state.studyForm.chelator,
    vector: state => state.studyForm.vector,
    target: state => state.studyForm.target,
    cellLine: state => state.studyForm.cellLine,
    mouseStrain: state => state.studyForm.mouseStrain,
    tumorModel: state => state.studyForm.tumorModel,
    radioActivity: state => state.studyForm.radioActivity,
    radioPurity: state => state.studyForm.radioPurity,
    comments: state => state.studyForm.comments,

    gammaForm: state => state.gammaForm,
    gammaCounter: state => state.gammaForm.gammaCounter,
    gammaCounterRunDateTime: state => state.gammaForm.gammaCounterRunDateTime,
    gammaCounterRunTimeOffset: state => state.gammaForm.gammaCounterRunTimeOffset,
    gammaCounterRunComments: state => state.gammaForm.gammaCounterRunComments,

    mice: state => state.mice,

    availableOrgans: state => state.availableOrgans,
    organCsv: state => state.organCsv,
    organForm: state => state.organForm,
    selectedOrgans: state => index => {
        return (index === -1) ? state.organForm.selectedOrgans : state.organForm.selectedOrgans[index]
    },

    loading: state => state.loading,
    error: state => state.error,
    mouseCsv: state => state.mouseCsv,
    mouseCsvJson: state => state.mouseCsvJson,
    biodiCsvs: state => state.biodiCsvs,
    biodiCsvJson: state => state.biodiCsvJson
};

export default {
    state: defaultState,
    getters,
    actions,
    mutations,
    namespaced: true
};