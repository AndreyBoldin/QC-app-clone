export interface ExcelData {
    jsonData: object
}

export interface Batch {
    id: number
    batch_num: number
    batch_date: string
    batch_normalized: boolean
}

export interface Project {
    id: number
    project_name: string
    project_date: string
}

export interface intraProjectInfo {
    jsonData: object
}
