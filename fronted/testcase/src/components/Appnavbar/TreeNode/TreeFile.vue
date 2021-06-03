<template>
  <div class="custom-tree-container">
    <el-input placeholder="输入关键字进行过滤" v-model="filterText"> </el-input>

    <div class="block">
      <p>
        测试用例集
        <span>
          <i @click="edit(data)" class="el-icon-edit"></i>
        </span>
      </p>
      <el-tree
        :data="data"
        node-key="id"
        :expand-on-click-node="false"
        :filter-node-method="filterNode"
        draggable
        accordion
        @node-click="OnChooseNode"
        ><template #default="{ node, data }">
          <span class="custom-tree-node">
            <span v-if="testif" span="100">
              <!--i @click="remove(node, data)" class="el-icon-delete"></i-->
              <el-checkbox> </el-checkbox
            ></span>
            <span>{{ node.label }} {{ data.id }}</span>
            <span>
              <!--i @click="edit(data)" class="el-icon-edit"></i-->
              <pop-over-operate
                v-bind:nodeInfo="nodeInfo"
                @click="OnChooseNode"
                :nowId="data.id"
                :nowLable="node.label"
              ></pop-over-operate>
              <!--i
                @click="addTestcase(node, data)"
                class="el-icon-circle-plus-outline"
              ></i-->
            </span>
          </span>
        </template>
      </el-tree>
    </div>
  </div>
</template>

<script>
import PopOverOperate from "../ChooseOption/PopOverOperate.vue";
let id = 1000;
export default {
  components: { PopOverOperate },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val);
    },
  },

  data() {
    const data = [
      {
        id: 1,
        label: "人脉",
        children: [
          {
            id: 4,
            label: "入口-1",
            children: [
              {
                id: 9,
                label: "功能-0",
              },
              {
                id: 10,
                label: "功能-1",
              },
            ],
          },
        ],
      },
      {
        id: 2,
        label: "形象",
        children: [
          {
            id: 5,
            label: "形象-入口1",
          },
          {
            id: 6,
            label: "形象-入口2",
            children: [
              {
                id: 9,
                label: "形象功能1",
              },
              {
                id: 10,
                label: "形象功能2",
              },
            ],
          },
        ],
      },
    ];
    return {
      nowid: "",
      nowLabel: "",
      filterText: "",
      data: JSON.parse(JSON.stringify(data)),
      testif: true,
      nodeInfo: {
        id: "test",
        nowid: this.nowid,
        nowLabel: this.nowLabel,
      },
    };
  },

  methods: {
    filterNode(value, data) {
      if (!value) return true;
      return data.label.indexOf(value) !== -1;
    },
    OnChooseNode(data) {
      (this.nowid = data.id), (this.nowLabel = data.label);
      console.log(data);
    },
    /*
            <el-button size="mini" on-click={() => this.append(store, data)}>
              Append
            </el-button>
            <el-button size="mini" on-click={() => this.remove(store, data)}>
              Delete
            </el-button>
    */
    renderContent(h, { node, data, store }) {
      return (
        <span>
          <span>
            <el-checkbox> </el-checkbox>
            <span>{node.label}</span>
          </span>
          <span style="float: right; margin-right: 20px"></span>
        </span>
      );
    },
    append(data) {
      const newChild = { id: id++, label: "testtest", children: [] };
      if (!data.children) {
        data.children = [];
      }
      data.children.push(newChild);
      this.data = [...this.data];
    },

    remove(node, data) {
      const parent = node.parent;
      const children = parent.data.children || parent.data;
      const index = children.findIndex((d) => d.id === data.id);
      children.splice(index, 1);
      this.data = [...this.data];
    },
    addTestcase() {},
  },
};
</script>

<style>
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}
</style>
