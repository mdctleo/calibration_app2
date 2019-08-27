import {
    getChelators,
    getCounters,
    getIsotopes,
    getMouseStrains,
    getTumorModels,
    getVectors,
    postBiodiCsv,
} from "../../../api/api";

const moment = require('moment');
const csv = require('csvtojson');


const getDefaultState = () => {
    return {
        studyForm: {
            studyName: "",
            studyDate: "",
            researcherName: "",
            piName: "",
            isotopeName: "",
            chelatorName: "",
            vectorName: "",
            target: "",
            mouseStrainName: "",
            tumorModelName: "",
            radioPurity: "",
            comment: "",
            numGammaRuns: ""
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
        biodiCsvs: [],
        biodiCsvFile: null,
        biodiCsvJson: null,
        loading: false,
        error: null,
        startValidation: false,
        mouseCsvFormat: "Mouse ID,Cage,Gender,Age,Group ID,Euthanasia Date,Euthanasia Time,Weight (g),Injection Date,Pre-Injection Time,Injection Time,Post-Injection Time,Pre-Injection MBq,Post-Injection MBq,Comments",
        mouseCsvs: [],
        mouseCsvJson: null,
        organCsvFormat: ",Group ID,\nTube ID,Mouse ID",
        organCsvs: [],
        organCsvJson: null,

        gammaCounters: [],
        isotopes: [],
        chelators: [],
        vectors: [],
        cellLines: [],
        mouseStrains: [],
        tumorModels: [],
    }
}

const state = getDefaultState()

const actions = {
    resetState: (context, payload) => {
        context.commit('RESET_STATE')
    },

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

    setIsotopeName: (context, payload) => {
        context.commit('SET_ISOTOPE_NAME', payload)
    },

    setChelatorName: (context, payload) => {
        context.commit('SET_CHELATOR_NAME', payload)
    },

    setVectorName: (context, payload) => {
        context.commit('SET_VECTOR_NAME', payload)
    },

    setTarget: (context, payload) => {
        context.commit('SET_TARGET', payload)
    },

    setMouseStrainName: (context, payload) => {
        context.commit('SET_MOUSE_STRAIN_NAME', payload)
    },

    setTumorModelName: (context, payload) => {
        context.commit('SET_TUMOR_MODEL_NAME', payload)
    },

    setRadioPurity: (context, payload) => {
        context.commit('SET_RADIO_PURITY', payload)
    },

    setComment: (context, payload) => {
        context.commit('SET_COMMENT', payload)
    },

    setNumGammaRuns: (context, payload) => {
        context.commit('SET_NUM_GAMMA_RUNS', payload)
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

    getIsotopes: (context) => {
        context.commit('SET_LOADING', {loading: true});
        getIsotopes()
            .then((response) => {
                context.commit('SET_ISOTOPES', {isotopes: response.data})
            })
            .catch((error) => {
                context.commit('SET_ERROR', {error: error.response.data.msg})
            })
            .finally(() => {
                context.commit('SET_LOADING', {loading: false});
            });
    },

    getChelators: (context) => {
        context.commit('SET_LOADING', {loading: true});
        getChelators()
            .then((response) => {
                context.commit('SET_CHELATORS', {chelators: response.data})
            })
            .catch((error) => {
                context.commit('SET_ERROR', {error: error.response.data.msg})
            })
            .finally(() => {
                context.commit('SET_LOADING', {loading: false});
            });
    },

    getVectors: (context) => {
        context.commit('SET_LOADING', {loading: true});
        getVectors()
            .then((response) => {
                context.commit('SET_VECTORS', {vectors: response.data})
            })
            .catch((error) => {
                context.commit('SET_ERROR', {error: error.response.data.msg})
            })
            .finally(() => {
                context.commit('SET_LOADING', {loading: false});
            });
    },

    getMouseStrains: (context) => {
        context.commit('SET_LOADING', {loading: true})
        getMouseStrains()
            .then((response) => {
                context.commit('SET_MOUSE_STRAINS', {mouseStrains: response.data})
            })
            .catch((error) => {
                context.commit('SET_ERROR', {error: error.response.data.msg})
            })
            .finally(() => {
                context.commit('SET_LOADING', {loading: false})
            })
    },

    getTumorModels: (context) => {
        context.commit('SET_LOADING', {loading: true})
        getTumorModels()
            .then((response) => {
                context.commit('SET_TUMOR_MODELS', {tumorModels: response.data})
            })
            .catch((error) => {
                context.commit('SET_ERROR', {error: error.response.data.msg})
            })
            .finally(() => {
                context.commit('SET_LOADING', {loading: false})
            })
    },

    getCounters: (context) => {
        context.commit('SET_LOADING', {loading: true})
        getCounters()
            .then((response) => {
                context.commit('SET_GAMMA_COUNTERS', {gammaCounters: response.data})
            })
            .catch((error) => {
                context.commit('SET_ERROR', {error: error.response.data.msg})
            })
            .finally(() => {
                context.commit('SET_LOADING', {loading: false})
            })
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

            fileReader.onload = (e) => {
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
        } else if (row['Euthanasia Time'] === "" || !moment(row['Euthanasia Time'], "HH:mm:ss", true).isValid()) {
            return {status: false, error: "Euthanasia Time validation failed"}
        } else if (row['Weight (g)'] === "") {
            return {status: false, error: "Weight validation failed"}
        } else if (row['Injection Date'] === "" || !moment(row['Injection Date'], "YYYY-MM-DD", true).isValid()) {
            return {status: false, error: "Injection Date validation failed"}
        } else if (row['Pre-Injection Time'] === "" || !moment(row['Pre-Injection Time'], "HH:mm:ss", true).isValid()) {
            return {status: false, error: "Pre-Injection Time validation failed"}
        } else if (row['Injection Time'] === "" || !moment(row['Injection Time'], "HH:mm:ss", true).isValid()) {
            return {status: false, error: "Injection Time validation failed"}
        } else if (row['Post-Injection Time'] === "" || !moment(row['Post-Injection Time'], "HH:mm:ss", true).isValid()) {
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
            if (payload.mouseCsvs.length === 0) {
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
            console.log(csvFileJson)
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
            context.commit('SET_ERROR', {error: err.msg})
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
            if (payload.organCsvs.length === 0) {
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
            context.commit('SET_ERROR', {error: err.msg});
            return false;
        } finally {
            context.commit('SET_LOADING', {loading: false});
        }
    },


    validateBiodiCsvs: (context, row) => {
        if (row['Protocol ID'] === "") {
            return false
        } else if (row['Measurement date & time'] === "" || !moment(row['Measurement date & time'], "YYYY-MM-DD HH:mm:ss", true).isValid()) {
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
        } else {
            return true
        }
    },

    handleBiodiCsvs: async (context, payload) => {
        try {
            context.commit('SET_LOADING', {loading: true})
            if (payload.biodiCsvs.length === 0) {
                context.commit('SET_ERROR', {error: "biodi csv not uploaded"})
                return false
            }

            let biodiCsvFile = payload.biodiCsvs[0]
            // let csvFile =  await context.dispatch('readFile', biodiCsvFile.raw)
            context.commit('SET_BIODI_CSV_FILE', {biodiCsvFile: biodiCsvFile.raw})
            return true
        } catch (error) {
            console.log(error)
            context.commit('SET_ERROR', {error: error.response.data.message})
            return false
        } finally {
            context.commit('SET_LOADING', {loading: false});
        }
    },

    postBiodiCsv(context, payload) {
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
    },

    async postBiodiCsvTest(context, payload) {
        try {
            context.commit('SET_LOADING', {loading: true})
            let result = await postBiodiCsv(payload)
        } catch (error) {
            context.commit('SET_ERROR', {error: error.response.data.message})
        } finally {
            context.commit('SET_LOADING', {loading: false})
        }
    }
};

const mutations = {
    RESET_STATE: (state) => {
        return Object.assign(state, getDefaultState())
    },
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

    SET_ISOTOPE_NAME: (state, payload) => {
        return state.studyForm.isotopeName = payload.isotopeName
    },

    SET_CHELATOR_NAME: (state, payload) => {
        return state.studyForm.chelatorName = payload.chelatorName
    },

    SET_VECTOR_NAME: (state, payload) => {
        return state.studyForm.vectorName = payload.vectorName
    },

    SET_TARGET: (state, payload) => {
        return state.studyForm.target = payload.target
    },

    SET_MOUSE_STRAIN_NAME: (state, payload) => {
        return state.studyForm.mouseStrainName = payload.mouseStrainName
    },

    SET_TUMOR_MODEL_NAME: (state, payload) => {
        return state.studyForm.tumorModelName = payload.tumorModelName
    },

    SET_RADIO_PURITY: (state, payload) => {
        return state.studyForm.radioPurity = payload.radioPurity
    },

    SET_COMMENT: (state, payload) => {
        return state.studyForm.comment = payload.comment
    },

    SET_NUM_GAMMA_RUNS: (state, payload) => {
        return state.studyForm.numGammaRuns = payload.numGammaRuns
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
    },

    SET_ISOTOPES: (state, payload) => {
        return state.isotopes = payload.isotopes
    },

    SET_CHELATORS: (state, payload) => {
        return state.chelators = payload.chelators
    },

    SET_VECTORS: (state, payload) => {
        return state.vectors = payload.vectors
    },

    SET_CELL_LINES: (state, payload) => {
        return state.cellLines = payload.cellLines
    },

    SET_MOUSE_STRAINS: (state, payload) => {
        return state.mouseStrains = payload.mouseStrains
    },

    SET_TUMOR_MODELS: (state, payload) => {
        return state.tumorModels = payload.tumorModels
    },

    SET_GAMMA_COUNTERS: (state, payload) => {
        return state.gammaCounters = payload.gammaCounters
    },

    SET_BIODI_CSV_FILE: (state, payload) => {
        return state.biodiCsvFile = payload.biodiCsvFile
    }
};

const getters = {
    startValidation: state => state.startValidation,

    studyForm: state => state.studyForm,
    studyName: state => state.studyForm.studyName,
    studyDate: state => state.studyForm.studyDate,
    researcherName: state => state.studyForm.researcherName,
    piName: state => state.studyForm.piName,
    isotopeName: state => state.studyForm.isotopeName,
    chelatorName: state => state.studyForm.chelatorName,
    vectorName: state => state.studyForm.vectorName,
    target: state => state.studyForm.target,
    mouseStrainName: state => state.studyForm.mouseStrainName,
    tumorModelName: state => state.studyForm.tumorModelName,
    radioPurity: state => state.studyForm.radioPurity,
    comment: state => state.studyForm.comment,
    numGammaRuns: state => state.studyForm.numGammaRuns,

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
    biodiCsvFile: state => state.biodiCsvFile,
    biodiCsvJson: state => state.biodiCsvJson,

    isotopes: state => state.isotopes,
    chelators: state => state.chelators,
    vectors: state => state.vectors,
    cellLines: state => state.cellLines,
    mouseStrains: state => state.mouseStrains,
    tumorModels: state => state.tumorModels,
    gammaCounters: state => state.gammaCounters
};

export default {
    state: state,
    getters,
    actions,
    mutations,
    namespaced: true
};