import {postBiodiCsvFile} from "../../../api/api";

const moment = require('moment');
const csv = require('csvtojson');

const defaultState = {
    studyName: "test",
    studyDate: "",
    researcherName: "",
    piName: "",
    radioIsotope: "",
    chelator: "",
    vector: "",
    target: "",
    radioActivity: "",
    radioPurity: "",
    comments: "",

    gammaCounters: [],
    mice: [],
    availableOrgans: [],
    biodiCsvs: null,
    biodiCsvJson: null,
    loading: false,
    error: null,
    startValidation: false,
    mouseCsvFormat: "Mouse ID, Group ID, Euthanasia Time, Weight (g), Injection Date, Pre-Injection Time, Injection Time, Post-Injection Time, Pre-Injection MBq, Post-Injection MBq, Comments",
    mouseCsv: null,
    mouseCsvJson: null,
    organCsvFormat: "Organ Order",
    organCsv: null,
    selectedOrgans: [],
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

    setRadioActivity: (context, payload) => {
        context.commit('SET_RADIO_ACTIVITY', payload)
    },

    setRadioPurity: (context, payload) => {
        context.commit('SET_RADIO_PURITY', payload)
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

    setMouseCsv: (context, payload) => {
        context.commit('SET_MOUSE_CSV', payload)
    },

    setOrganCsv: (context, payload) => {
        context.commit('SET_ORGAN_CSV', payload)
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
        if (row['Euthanasia Time'] === "") {
            return false;
        } else if (row['Group ID'] === "") {
            return false;
        } else if (row['Injection Date'] === "") {
            return false;
        } else if (row['Injection Time'] === "") {
            return false;
        } else if (row['Mouse ID'] === "") {
            return false;
        } else if (row['Post-Injection MBq'] === "") {
            return false;
        } else if (row['Pre-Injection MBq'] === "") {
            return false;
        } else if (row['Pre-Injection Time'] === "") {
            return false;
        } else if (row['Weight (g)'] === "") {
            return false;
        } else {
            return true;
        }
    },


    handleMouseCsv: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true});
            // did not upload file
            if (payload.mouseCsv === null) {
                context.commit('SET_ERROR', {error: "Form not uploaded"});
                return false;
            }
            let mouseCsv = payload.mouseCsv[0].raw;

            let csvFile = await context.dispatch('readFile', mouseCsv);
            // validate headers
            if (csvFile.substring(0, context.state.mouseCsvFormat.length) !== context.state.mouseCsvFormat) {
                context.commit('SET_ERROR', {error: "Do not mess with the headers"});
                return false;
            }
            let csvFileJson = await csv().fromString(csvFile);
            let indexHolder = 0;
            let rowValidation = true;

            // validate each existing rows for required cells
            for (let i = 0; i < csvFileJson.length; i++) {
                let row = csvFileJson[i];
                indexHolder = i;
                rowValidation = await context.dispatch('validateMouse', row);

                if (!rowValidation) {
                    break;
                }
            }

            if (rowValidation) {
                return true;
            } else {
                context.commit('SET_ERROR', {error: "There is an error on row " + (indexHolder + 2)});
                return false;
            }
        } catch (err) {
            context.commit('SET_ERROR', {error: err.message});
            return false;
        } finally {
            context.commit('SET_LOADING', {loading: false});
        }
    },

    // validateOrgan: (context, row, availableOrgans) => {
    //     return availableOrgans.includes(row['Organ Order']);
    // },

    handleOrganCsv: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true});
            if (payload.organCsv === null) {
                context.commit('SET_ERROR', {error: "Form not uploaded"});
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

    /**
     * File upload start
     **/
    handleBiodiCsv: (context, payload) => {
        context.commit('SET_LOADING', {loading: true});
        let biodiCsvFile = payload.biodiCsvs[0]
        context.dispatch('readFile', biodiCsvFile.raw)
            .then((csvFile) => {
                return csv().fromString(csvFile)
            })
            .then((csvFileJson) => {
                let fileFormat = {
                    fileName: biodiCsvFile.name,
                    file: csvFileJson
                };

                return postBiodiCsvFile(fileFormat)
            })
            .then((response) => {

            })
            .catch((error) => {
                context.commit('SET_ERROR', {error: error.response.data.message})
            })
            .finally(() => {
                context.commit('SET_LOADING', {loading: false});
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

    SET_CHELATOR: (state, payload) => {
        return state.chelator = payload.chelator
    },

    SET_VECTOR: (state, payload) => {
        return state.vector = payload.vector
    },

    SET_TARGET: (state, payload) => {
        return state.target = payload.target
    },

    SET_CELL_LINE: (state, payload) => {
        return state.cellLine = payload.cellLine
    },

    SET_RADIO_ACTIVITY: (state, payload) => {
        return state.radioActivity = payload.radioActivity
    },

    SET_RADIO_PURITY: (state, payload) => {
        return state.radioPurity = payload.radioPurity
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

    SET_AVAILABLE_ORGANS: (state, payload) => {
        return state.availableOrgans = payload.availableOrgans
    },

    SET_SELECTED_ORGANS: (state, payload) => {
        return state.selectedOrgans = payload.selectedOrgans
    },

    SET_MOUSE_CSV: (state, payload) => {
        return state.mouseCsv = payload.mouseCsv
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
    studyName: state => state.studyName,
    studyDate: state => state.studyDate,
    researcherName: state => state.researcherName,
    piName: state => state.piName,
    radioIsotope: state => state.radioIsotope,
    radioTracer: state => state.radioTracer,
    chelator: state => state.chelator,
    vector: state => state.vector,
    target: state => state.target,
    cellLine: state => state.cellLine,
    comments: state => state.comments,
    gammaCounters: state => state.gammaCounters,
    mice: state => state.mice,
    availableOrgans: state => state.availableOrgans,
    loading: state => state.loading,
    error: state => state.error,
    mouseCsv: state => state.mouseCsv,
    organCsv: state => state.organCsv,
    selectedOrgans: state => state.selectedOrgans,
    biodiCsvs: state => state.biodiCsvs
};

export default {
    state: defaultState,
    getters,
    actions,
    mutations,
    namespaced: true
};