<template>
    <span>{{parentObj.name}}</span>
</template>
<script>
export default {
    inject:['parentObj'],
    setup() {
        
    },
    updated() {
        if(this.parentObj.name=="Jack"){
            this.parentObj.name ="test2222"
        }
        console.log(this.parentObj.name)
        console.log(this.parentObj.test)
    },
}
</script>