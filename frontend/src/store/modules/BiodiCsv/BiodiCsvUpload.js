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
        radioPurity: "",
        comments: "",
    },

    gammaForm: {
        gammaCounter: "",
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
    mouseCsvFormat: "Mouse ID, Cage, Gender, Age, Group ID, Euthanasia Date, Euthanasia Time, Weight (g), Injection Date, Pre-Injection Time, Injection Time, Post-Injection Time, Pre-Injection MBq, Post-Injection MBq, Comments",
    mouseCsvs: null,
    mouseCsvJson: null,
    organCsvFormat: " , Group ID, \n Tube ID, Mouse ID",
    organCsvs: null,
    organCsvJson: null
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

    setRadioPurity: (context, payload) => {
        context.commit('SET_RADIO_PURITY', payload)
    },

    setComments: (context, payload) => {
        context.commit('SET_COMMENTS', payload)
    },

    setGammaCounter: (context, payload) => {
        context.commit('SET_GAMMA_COUNTER', payload)
    },

    setGammaCounterRunTimeOffset: (context, payload) => {
        context.commit('SET_GAMMA_COUNTER_RUN_TIME_OFFSET', payload)
    },

    setGammaCounterRunComments: (context, payload) => {
        context.commit('SET_GAMMA_COUNTER_RUN_COMMENTS', payload)
    },

    setMouseCsvs: (context, payload) => {
        context.commit('SET_MOUSE_CSVS', payload)
    },

    setOrganCsvs: (context, payload) => {
        context.commit('SET_ORGAN_CSVS', payload)
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
            return {status: false, error: "Mouse ID validation failed"}
        } else if (row['Gender'] !== "M" && row['Gender'] !== "F") {
            return {status: false, error: "Gender validation failed"}
        } else if (row['Age'] === "") {
            return {status: false, error: "Age validation failed"}
        } else if (row['Group ID'] === "") {
            return {status: false, error: "Group ID validation failed"}
        } else if (row['Euthanasia Date'] === "" || !moment(row['Euthanasia Date'], "YYYY-MM-DD", true).isValid()) {
            return {status: false, error: "Euthanasia Date validation failed"}
        } else if (row['Euthanasia Time'] === "" || !moment(row['Euthanasia Time'], "HH:mm", true).isValid()) {
            return {status: false, error: "Euthanasia Time validation failed"}
        } else if (row['Weight (g)'] === "") {
            return {status: false, error: "Weight validation failed"}
        } else if (row['Injection Date'] === "" || !moment(row['Injection Date'], "YYYY-MM-DD", true).isValid()) {
            return {status: false, error: "Injection Date validation failed"}
        } else if (row['Pre-Injection Time'] === "" || !moment(row['Pre-Injection Time'], "HH:mm", true).isValid()) {
            return {status: false, error: "Pre-Injection Time validation failed"}
        } else if (row['Injection Time'] === "" || !moment(row['Injection Time'], "HH:mm", true).isValid()) {
            return {status: false, error: "Injection Time validation failed"}
        } else if (row['Post-Injection Time'] === "" || !moment(row['Post-Injection Time'], "HH:mm", true).isValid()) {
            return {status: false, error: "Post-Injection Time validation failed"}
        } else if (row['Pre-Injection MBq'] === "") {
            return {status: false, error: "Pre-Injection MBq validation failed"}
        } else if (row['Post-Injection MBq'] === "") {
            return {status: false, error: "Post-Injection MBq validation failed"}
        } else {
            return {status: true, error: null}
        }
    },


    handleMouseCsvs: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true})
            // did not upload file
            if (payload.mouseCsvs === null) {
                context.commit('SET_ERROR', {error: "mouse csv not uploaded"})
                return false
            }
            let mouseCsv = payload.mouseCsvs[0].raw

            let csvFile = await context.dispatch('readFile', mouseCsv)
            // validate headers
            if (csvFile.substring(0, context.state.mouseCsvFormat.length) !== context.state.mouseCsvFormat) {
                context.commit('SET_ERROR', {error: "Do not mess with mouse csv headers"})
                return false
            }
            let csvFileJson = await csv().fromString(csvFile)
            let indexHolder = 0
            let rowValidated = true

            if (csvFileJson.length === 0) {
                context.commit('SET_ERROR', {error: "mouse csv empty"})
                return false
            }

            // validate each existing rows for required cells
            for (let i = 0; i < csvFileJson.length; i++) {
                let row = csvFileJson[i]
                indexHolder = i
                rowValidated = await context.dispatch('validateMouse', row)

                if (!rowValidated.status) {
                    break
                }
            }

            if (rowValidated.status) {
                context.commit('SET_MOUSE_CSV_JSON', {mouseCsvJson: csvFileJson})
                return true
            } else {
                context.commit('SET_ERROR', {error: rowValidated.error + " in mouse csv on row " + (indexHolder + 2)})
                return false
            }
        } catch (err) {
            context.commit('SET_ERROR', {error: err.message})
            return false
        } finally {
            context.commit('SET_LOADING', {loading: false})
        }
    },

    validateOrgan: async (context, payload) => {
        let row = payload.row
        if (row['mouseId'] === "" || row['mouseId'] === undefined) {
            return false
        } else if (row['groupId'] === "" || row['groupId'] === undefined) {
            return false
        } else {
            return true
        }
    },

    parseOrganCsv: async (context, payload) => {
        let csvFile = payload.organCsv.trim()

        let csvFileMatrix = csvFile.split("\n")

        for (let i = 0; i < csvFileMatrix.length; i++) {
            csvFileMatrix[i] = csvFileMatrix[i].split(",")
        }

        let jLength = csvFileMatrix[0].length
        let iLength = csvFileMatrix.length
        let output = []

        for (let j = 2; j < jLength; j++) {
            let organObj = {}
            for (let i = 1; i < iLength; i++) {
                if (i === 1) {
                    organObj.mouseId = csvFileMatrix[i][j]
                    organObj.groupId = csvFileMatrix[0][j]
                    organObj.organs = []
                } else {
                    let tubeId = csvFileMatrix[i][0]
                    let organ = csvFileMatrix[i][1]
                    let organMass = csvFileMatrix[i][j]
                    if (organObj.organs[tubeId - 1] === undefined) {
                        organObj.organs[tubeId - 1] = {organ: organ, organMass: organMass}
                    } else {
                        throw Error('Duplicate tube Id for organ Csv, parsing failed')
                    }

                }
            }
            output.push(organObj)
        }

        return output
    },

    handleOrganCsvs: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true});
            if (payload.organCsvs === null) {
                context.commit('SET_ERROR', {error: "organ csv not uploaded"});
                return context.commit('SET_SELECTED_ORGANS', {selectedOrgans: []})
            }

            let organCsv = payload.organCsvs[0].raw;

            organCsv = await context.dispatch('readFile', organCsv);

            let organCsvJson = await context.dispatch('parseOrganCsv', {organCsv: organCsv})

            let rowValidated = true
            for (let i = 0; i < organCsvJson.length; i++) {
                let row = organCsvJson[i]
                rowValidated = await context.dispatch('validateOrgan', {row: row})

                if (!rowValidated) {
                    break
                }

            }

            if (rowValidated) {
                context.commit('SET_ORGAN_CSV_JSON', {organCsvJson: organCsvJson})
                return true
            } else {
                context.commit('SET_ERROR', {error: "There is an error  wirth your organ_order csv"})
                return false
            }

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

            if (csvFileJson.length === 0) {
                context.commit('SET_ERROR', {error: "biodii csv empty"})
                return false
            }


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
                context.commit('SET_ERROR', {error: "There is an error in biodi csv on row " + (indexHolder + 2)})
                return false

            }

        } catch (error) {
            context.commit('SET_ERROR', {error: error.response.data.message})
            return false
        } finally {
            context.commit('SET_LOADING', {loading: false});
        }
    },

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

    SET_RADIO_PURITY: (state, payload) => {
        return state.studyForm.radioPurity = payload.radioPurity
    },

    SET_COMMENTS: (state, payload) => {
        return state.studyForm.comments = payload.comments
    },

    SET_GAMMA_COUNTER: (state, payload) => {
        return state.gammaForm.gammaCounter = payload.gammaCounter
    },

    SET_GAMMA_COUNTER_RUN_TIME_OFFSET: (state, payload) => {
        return state.gammaForm.gammaCounterRunTimeOffset = payload.gammaCounterRunTimeOffset
    },

    SET_GAMMA_COUNTER_RUN_COMMENTS: (state, payload) => {
        return state.gammaForm.gammaCounterRunComments = payload.gammaCounterRunComments
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

    SET_MOUSE_CSVS: (state, payload) => {
        return state.mouseCsvs = payload.mouseCsvs
    },

    SET_MOUSE_CSV_JSON: (state, payload) => {
        return state.mouseCsvJson = payload.mouseCsvJson
    },

    SET_ORGAN_CSVS: (state, payload) => {
        return state.organCsvs = payload.organCsvs
    },

    SET_ORGAN_CSV_JSON: (state, payload) => {
        return state.organCsvJson = payload.organCsvJson
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
    radioPurity: state => state.studyForm.radioPurity,
    comments: state => state.studyForm.comments,

    gammaForm: state => state.gammaForm,
    gammaCounter: state => state.gammaForm.gammaCounter,
    gammaCounterRunTimeOffset: state => state.gammaForm.gammaCounterRunTimeOffset,
    gammaCounterRunComments: state => state.gammaForm.gammaCounterRunComments,

    mice: state => state.mice,

    availableOrgans: state => state.availableOrgans,
    organCsvs: state => state.organCsvs,
    organCsvJson: state => state.organCsvJson,
    organForm: state => state.organForm,
    selectedOrgans: state => index => {
        return (index === -1) ? state.organForm.selectedOrgans : state.organForm.selectedOrgans[index]
    },

    loading: state => state.loading,
    error: state => state.error,
    mouseCsvs: state => state.mouseCsvs,
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