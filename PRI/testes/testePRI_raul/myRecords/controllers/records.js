var Record = require('../models/records')
const Records= module.exports
// var mongoose = require('mongoose')

Records.list = () => {
    return Record
        .find()
        .exec()
}

// alinea 1
// lista as atividades no dataset com os seguintes campos: data, tipo de atividade, distância em Km e tempo;
Records.listarAtividades = () => {
    return Record
        .find({},{
            _id:0,
            start_date:1,
            type:1,
            distance:1,
            elapsed_time:1,
        })
        .exec()
}


// alinea 2
//vlista as atividades que pertencem ao tipo indicado;
Records.listarTipo = (t) => {
    return Record
        .find({type:t})
        .exec()
}

// alinea 3
// - devolve a atividade com a duração mais longa;
Records.AtividadeMaisLonga = () => {
    return Record
        .find()
        .sort({ elapsed_time:-1 })
        .limit(1)
        .exec()
}

// alinea 4
// devolve a atividade mais longa do tipo indicado.
Records.AtividadeEspecificaMaisLonga = (t) => {
    return Record
        .find({type:t})
        .sort({ elapsed_time: -1 })
        .limit(1)
        .exec()
}


// // 1 alinea
// Premios.listarYC = () =>{
//     return Premio
//         .find({},{
//             year:1,
//             category:1
//         })
//         .exec()
// }
// // 2 alinea importante ObjectId (ver no compass)
// Premios.listarID = id => {
//     return Premio
//         .findOne({_id: mongoose.Types.ObjectId(id)})
//         .exec()
// }

// // 3 alinea Devolve a lista de categorias, sem repetições;
// Premios.listarCat = () => {
//     return Premio
//         .distinct("category")
//         .exec()
// }

// // 4 alinea - Devolve a lista de prémios que tenham o campo "category" com o valor "YYY"
// Premios.listarCatX = cat => {
//     return Premio
//         .find({category:cat})
//         .exec()
// }

// // 5 alinea  Devolve a lista de prémios que tenham o campo "category"
// // com o valor "YYY" e o campo "year" com um valor superior a "AAAA";
// Premios.listarCatYear = (cat,y) => {
//     return Premio
//         .find({ category: cat, year:{$gte:y}})
//         .exec()
// }

// // 6 alinea Devolve uma lista ordenada alfabeticamente por nome dos
// // laureados com os campos correspondentes ao nome, ano do prémio e categoria.
// // com o valor "YYY" e o campo "year" com um valor superior a "AAAA";

// //(not done)
// Premios.listarLaureados = () => {
//     return Premio
//         .find({},{
//             "laureates.firstname": 1,
//             "laureates.surname": 1,
//             // another way
//             // laureados: {
//             //     firstname: 1,
//             //     surname: 1
//             // }
//             year:1,
//             category:1
//         })
//         .sort({"laureates.firstname":1})
//         .exec()
// }


// // Comps.listarCompositor = id => {
// //     return Comp
// //         .findOne({_id:id})
// //         .exec()
// // }


// // Comps.listarPeriodo = (p) => {
// //     return Comp
// //         .find({periodo:p})
// //         .exec()
// // }


// // Comps.listarPeriodoNasc = (p,d) => {
// //     return Comp
// //         // .find({ periodo: p ,  dataNasc: { $gte: d }})
// //         .find({ periodo: p})
// //         .find({dataNasc:{$gte:d}})

// //         .exec()
// // }
